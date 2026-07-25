from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from .evidence import EvidenceLedger, build_credit_event, build_evidence_event, request_digest
from .models import ActionRequest, PAACContract, ConfirmationRecord, RevocationRegistry
from .policy import PolicyEvaluator


class Decision(str, Enum):
    ALLOW = "ALLOW"
    ALLOW_WITH_LOG = "ALLOW_WITH_LOG"
    REQUIRE_CONFIRMATION = "REQUIRE_CONFIRMATION"
    BLOCK = "BLOCK"


class EnforcementEngine:
    """Deterministic local reference enforcement layer for PATL v0.1 alpha."""

    def __init__(
        self,
        contracts: dict[str, PAACContract],
        ledger: EvidenceLedger | None = None,
        revocations: RevocationRegistry | None = None,
        confirmations: dict[str, ConfirmationRecord] | None = None,
        now: datetime | None = None,
    ) -> None:
        self.contracts = contracts
        self.ledger = ledger or EvidenceLedger()
        self.revocations = revocations or RevocationRegistry()
        self.confirmations = confirmations or {}
        self.now = now
        self.policy = PolicyEvaluator()
        self._seen_replay_keys: set[str] = set()

    def evaluate(self, request: ActionRequest) -> dict[str, Any]:
        evaluated_at = self._evaluation_time(request)
        contract = self.contracts.get(request.contract_id)
        reasons: list[str] = []
        violations: list[str] = []

        if contract is None:
            decision = Decision.BLOCK
            reasons.append("contract_not_found")
            violations.append("missing_authorization")
        else:
            decision, reasons, violations = self._evaluate_with_contract(contract, request)

        evidence = build_evidence_event(
            request=request,
            decision=decision.value,
            reasons=reasons,
            violations=violations,
            policy_version=self.policy.version,
            evaluated_at=evaluated_at,
            previous_event_hash=self.ledger.last_hash(),
        )
        self.ledger.append(evidence)
        credit_event = build_credit_event(evidence)
        return {
            "decision": decision.value,
            "reasons": reasons,
            "violations": violations,
            "evidence": evidence,
            "agent_credit_event": credit_event,
        }

    def _evaluate_with_contract(
        self, contract: PAACContract, request: ActionRequest
    ) -> tuple[Decision, list[str], list[str]]:
        reasons: list[str] = []
        violations: list[str] = []

        evaluated_at = self._evaluation_time(request)
        replay_key = request_digest(request)
        if replay_key in self._seen_replay_keys or request.request_id in contract.used_request_ids:
            return Decision.BLOCK, ["replay_detected"], ["replay"]

        if self.revocations.is_revoked(contract.contract_id, request.agent_id):
            return Decision.BLOCK, ["authorization_revoked"], ["revocation_bypass_attempt"]

        if not contract.is_active_at(evaluated_at):
            return Decision.BLOCK, ["contract_expired_or_not_yet_valid"], ["expired_authorization"]

        if request.agent_id != contract.agent_id:
            return Decision.BLOCK, ["agent_identity_mismatch"], ["agent_mismatch"]

        if request.metadata.get("agent_version") != contract.agent_version:
            return Decision.BLOCK, ["agent_version_mismatch"], ["agent_version_mismatch"]

        if request.metadata.get("model_id") != contract.model_id:
            return Decision.BLOCK, ["model_identity_mismatch"], ["model_mismatch"]

        tool_id = request.metadata.get("tool_id")
        if tool_id not in contract.tool_ids:
            return Decision.BLOCK, ["tool_not_declared"], ["undeclared_tool"]

        delegated_agent_id = request.metadata.get("delegated_agent_id")
        allowed_delegates = set(contract.resources.get("allowed_delegated_agent_ids", []))
        if delegated_agent_id and delegated_agent_id not in allowed_delegates:
            return Decision.BLOCK, ["delegation_not_declared"], ["undeclared_delegation"]

        if request.action_type in contract.prohibited_actions:
            return Decision.BLOCK, ["action_explicitly_prohibited"], ["prohibited_action"]

        if request.action_type not in contract.permitted_actions:
            return Decision.BLOCK, ["action_not_permitted"], ["permission_mismatch"]

        policy_result = self.policy.evaluate(contract, request)
        reasons.extend(policy_result.reasons)
        violations.extend(policy_result.violations)

        if policy_result.block:
            return Decision.BLOCK, reasons, violations

        confirmation_needed = policy_result.requires_confirmation or request.action_type in contract.confirmation_required_actions
        if confirmation_needed and not self._has_valid_confirmation(contract, request):
            return Decision.REQUIRE_CONFIRMATION, reasons + ["confirmation_required"], violations

        max_execution_count = int(contract.constraints.get("max_execution_count", 0) or 0)
        if max_execution_count and contract.execution_count >= max_execution_count:
            return Decision.BLOCK, ["execution_count_exhausted"], ["execution_budget_exhausted"]

        self._seen_replay_keys.add(replay_key)
        contract.used_request_ids.add(request.request_id)
        contract.execution_count += 1

        if request.action_type in contract.log_required_actions or policy_result.log_required:
            return Decision.ALLOW_WITH_LOG, reasons + ["within_scope_logged"], violations

        return Decision.ALLOW, reasons + ["within_scope"], violations

    def _has_valid_confirmation(self, contract: PAACContract, request: ActionRequest) -> bool:
        confirmation = self.confirmations.get(request.request_id)
        if confirmation is None:
            return False
        evaluated_at = self._evaluation_time(request)
        return (
            confirmation.contract_id == contract.contract_id
            and confirmation.request_id == request.request_id
            and confirmation.request_digest == request_digest(request)
            and confirmation.nonce == request.metadata.get("confirmation_nonce")
            and confirmation.confirmed
            and confirmation.confirmed_by == "user"
            and confirmation.is_active_at(evaluated_at)
        )

    def _evaluation_time(self, request: ActionRequest) -> datetime:
        when = self.now or request.created_at or datetime.now(timezone.utc)
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        return when
