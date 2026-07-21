from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any

from .models import ActionRequest, PAACContract


@dataclass
class PolicyResult:
    block: bool = False
    requires_confirmation: bool = False
    log_required: bool = False
    reasons: list[str] | None = None
    violations: list[str] | None = None

    def __post_init__(self) -> None:
        self.reasons = self.reasons or []
        self.violations = self.violations or []


class PolicyEvaluator:
    version = "patl-policy-v0.1-alpha"

    def evaluate(self, contract: PAACContract, request: ActionRequest) -> PolicyResult:
        result = PolicyResult()
        action = request.action_type
        if action.startswith("email."):
            self._email(contract, request, result)
        elif action.startswith("travel."):
            self._travel(contract, request, result)
        elif action.startswith("file."):
            self._file(contract, request, result)
        else:
            result.block = True
            result.reasons.append("unknown_action_family")
            result.violations.append("unknown_action")
        return result

    def _email(self, contract: PAACContract, request: ActionRequest, result: PolicyResult) -> None:
        allowed_domains = set(contract.resources.get("email_allowed_recipient_domains", []))
        recipients = request.params.get("recipients", [])
        if recipients and allowed_domains:
            for recipient in recipients:
                domain = recipient.split("@")[-1].lower()
                if domain not in allowed_domains:
                    result.block = True
                    result.reasons.append("email_recipient_domain_out_of_scope")
                    result.violations.append("unexpected_recipient")
        if request.action_type == "email.send":
            result.requires_confirmation = True
        if request.params.get("contains_sensitive_data"):
            result.requires_confirmation = True
            result.log_required = True
            result.reasons.append("sensitive_content_requires_confirmation")

    def _travel(self, contract: PAACContract, request: ActionRequest, result: PolicyResult) -> None:
        max_amount = float(contract.constraints.get("max_payment_amount", 0))
        amount = float(request.params.get("amount", 0))
        if request.action_type == "travel.purchase" and amount > max_amount:
            result.block = True
            result.reasons.append("payment_amount_exceeds_contract_limit")
            result.violations.append("payment_limit_exceeded")
        elif request.action_type == "travel.purchase":
            result.requires_confirmation = True
            result.log_required = True
        allowed_currencies = set(contract.constraints.get("allowed_currencies", []))
        currency = request.params.get("currency")
        if currency and allowed_currencies and currency not in allowed_currencies:
            result.block = True
            result.reasons.append("currency_out_of_scope")
            result.violations.append("currency_mismatch")

    def _file(self, contract: PAACContract, request: ActionRequest, result: PolicyResult) -> None:
        path = request.params.get("path") or request.resource
        scopes = [PurePosixPath(s) for s in contract.resources.get("file_allowed_paths", [])]
        target = PurePosixPath(path)
        if scopes and not any(self._under(target, scope) for scope in scopes):
            result.block = True
            result.reasons.append("file_path_out_of_scope")
            result.violations.append("path_scope_violation")
        if request.action_type in {"file.delete", "file.upload"}:
            if request.action_type in contract.prohibited_actions:
                result.block = True
                result.reasons.append("irreversible_or_exfiltration_action_prohibited")
                result.violations.append("blocked_file_operation")
            else:
                result.requires_confirmation = True
                result.log_required = True

    @staticmethod
    def _under(target: PurePosixPath, scope: PurePosixPath) -> bool:
        return target == scope or scope in target.parents
