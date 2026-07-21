from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable

from .evidence import EvidenceLedger, build_credit_event, build_evidence_event, request_digest
from .models import ActionRequest, ConfirmationRecord, PAACContract, RequestStatus, RevocationRegistry
from .policy import PolicyEvaluator


class Decision(str, Enum):
    ALLOW = "ALLOW"
    ALLOW_WITH_LOG = "ALLOW_WITH_LOG"
    REQUIRE_CONFIRMATION = "REQUIRE_CONFIRMATION"
    BLOCK = "BLOCK"


class EnforcementEngine:
    """Deterministic local reference enforcement layer for PATL v0.1.1 alpha."""

    def __init__(
        self,
        contracts: dict[str, PAACContract],
        ledger: EvidenceLedger | None = None,
        revocations: RevocationRegistry | None = None,
        confirmations: dict[str, ConfirmationRecord] | None = None,
        now: datetime | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self.contracts = contracts
        if clock is None and now is not None:
            clock = lambda: now
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self.ledger = ledger or EvidenceLedger(clock=self.clock)
        self.revocations = revocations or RevocationRegistry()
        self.confirmations = confirmations if confirmations is not None else {}
        self.policy = PolicyEvaluator()
        self.request_status: dict[str, RequestStatus] = {}
        self.request_digests: dict[str, str] = {}

    def evaluate(self, request: ActionRequest) -> dict[str, Any]:
        evaluated_at = self._now()
        digest_value = request_digest(request)
        contract = self.contracts.get(request.contract_id)
        reasons: list[str] = []
        violations: list[str] = []

        if contract is None:
            decision = Decision.BLOCK
            reasons.append("contract_not_found")
            violations.append("missing_authorization")
            lifecycle_status = RequestStatus.BLOCKED
            lifecycle_transitions = [RequestStatus.PENDING, RequestStatus.BLOCKED]
        else:
            decision, reasons, violations, lifecycle_status, lifecycle_transitions = self._evaluate_with_contract(
                contract, request, evaluated_at, digest_value
            )

        evidence = build_evidence_event(
            request=request,
            decision=decision.value,
            lifecycle_status=lifecycle_status.value,
            lifecycle_transitions=[status.value for status in lifecycle_transitions],
            request_digest_value=digest_value,
            reasons=reasons,
            violations=violations,
            policy_version=self.policy.version,
            evaluated_at=evaluated_at,
        )
        ledger_record = self.ledger.append(evidence)
        credit_event = build_credit_event(evidence)
        return {
            "decision": decision.value,
            "lifecycle_status": lifecycle_status.value,
            "lifecycle_transitions": [status.value for status in lifecycle_transitions],
            "reasons": reasons,
            "violations": violations,
            "evidence": evidence,
            "ledger_record": ledger_record,
            "agent_credit_event": credit_event,
        }

    def _evaluate_with_contract(
        self, contract: PAACContract, request: ActionRequest, evaluated_at: datetime, digest_value: str
    ) -> tuple[Decision, list[str], list[str], RequestStatus, list[RequestStatus]]:
        reasons: list[str] = []
        violations: list[str] = []
        key = self._request_key(request)
        previous_status = self.request_status.get(key)
        transitions = [previous_status or RequestStatus.PENDING]

        if previous_status == RequestStatus.CONSUMED:
            return self._finish(
                key,
                RequestStatus.BLOCKED,
                Decision.BLOCK,
                ["replay_detected"],
                ["replay"],
                transitions,
                stored_status=RequestStatus.CONSUMED,
            )

        previous_digest = self.request_digests.get(key)
        if previous_status == RequestStatus.AWAITING_CONFIRMATION and previous_digest != digest_value:
            return self._finish(
                key,
                RequestStatus.BLOCKED,
                Decision.BLOCK,
                ["pending_request_digest_changed"],
                ["parameter_substitution"],
                transitions,
                stored_status=RequestStatus.BLOCKED,
            )

        if self.revocations.is_revoked(contract.contract_id, request.agent_id) or contract.revoked:
            return self._finish(
                key,
                RequestStatus.REVOKED,
                Decision.BLOCK,
                ["authorization_revoked"],
                ["revocation_bypass_attempt"],
                transitions,
            )

        if not contract.is_active_at(evaluated_at):
            return self._finish(
                key,
                RequestStatus.EXPIRED,
                Decision.BLOCK,
                ["contract_expired_or_not_yet_valid"],
                ["expired_authorization"],
                transitions,
            )

        stack_block = self._agent_stack_violations(contract, request)
        if stack_block:
            reason, violation = stack_block
            return self._finish(key, RequestStatus.BLOCKED, Decision.BLOCK, [reason], [violation], transitions)

        if not contract.executions_available():
            return self._finish(
                key,
                RequestStatus.BLOCKED,
                Decision.BLOCK,
                ["maximum_executions_exceeded"],
                ["execution_limit_exceeded"],
                transitions,
            )

        if request.action_type in contract.prohibited_actions:
            return self._finish(
                key,
                RequestStatus.BLOCKED,
                Decision.BLOCK,
                ["action_explicitly_prohibited"],
                ["prohibited_action"],
                transitions,
            )

        if request.action_type not in contract.permitted_actions:
            return self._finish(
                key,
                RequestStatus.BLOCKED,
                Decision.BLOCK,
                ["action_not_permitted"],
                ["permission_mismatch"],
                transitions,
            )

        policy_result = self.policy.evaluate(contract, request)
        reasons.extend(policy_result.reasons)
        violations.extend(policy_result.violations)

        if policy_result.block:
            return self._finish(key, RequestStatus.BLOCKED, Decision.BLOCK, reasons, violations, transitions)

        confirmation_needed = policy_result.requires_confirmation or request.action_type in contract.confirmation_required_actions
        if confirmation_needed:
            confirmation_decision = self._confirmation_decision(contract, request, evaluated_at, digest_value)
            if confirmation_decision is not None:
                decision, reason, violation, status = confirmation_decision
                return self._finish(
                    key,
                    status,
                    decision,
                    reasons + [reason],
                    violations + ([violation] if violation else []),
                    transitions,
                    digest_value=digest_value,
                    consume=False,
                )

        transitions.extend([RequestStatus.AUTHORIZED, RequestStatus.EXECUTED])
        contract.execution_count += 1
        if request.action_type in contract.log_required_actions or policy_result.log_required:
            return self._finish(
                key,
                RequestStatus.CONSUMED,
                Decision.ALLOW_WITH_LOG,
                reasons + ["within_scope_logged"],
                violations,
                transitions,
                digest_value=digest_value,
                consume=True,
            )

        return self._finish(
            key,
            RequestStatus.CONSUMED,
            Decision.ALLOW,
            reasons + ["within_scope"],
            violations,
            transitions,
            digest_value=digest_value,
            consume=True,
        )

    def _confirmation_decision(
        self, contract: PAACContract, request: ActionRequest, evaluated_at: datetime, digest_value: str
    ) -> tuple[Decision, str, str | None, RequestStatus] | None:
        confirmation = self.confirmations.get(request.request_id)
        if confirmation is None:
            return Decision.REQUIRE_CONFIRMATION, "confirmation_required", None, RequestStatus.AWAITING_CONFIRMATION
        if confirmation.contract_id != contract.contract_id or confirmation.request_id != request.request_id:
            return Decision.BLOCK, "confirmation_scope_mismatch", "confirmation_scope_mismatch", RequestStatus.BLOCKED
        if not confirmation.confirmed or confirmation.confirmed_by != "user":
            return Decision.BLOCK, "confirmation_denied_or_untrusted", "invalid_confirmation", RequestStatus.BLOCKED
        if not confirmation.is_active_at(evaluated_at):
            return Decision.REQUIRE_CONFIRMATION, "confirmation_expired", None, RequestStatus.AWAITING_CONFIRMATION
        if confirmation.request_digest != digest_value:
            return (
                Decision.BLOCK,
                "confirmation_request_digest_mismatch",
                "parameter_substitution",
                RequestStatus.BLOCKED,
            )
        return None

    @staticmethod
    def _request_key(request: ActionRequest) -> str:
        return f"{request.contract_id}:{request.request_id}"

    def _finish(
        self,
        key: str,
        status: RequestStatus,
        decision: Decision,
        reasons: list[str],
        violations: list[str],
        transitions: list[RequestStatus],
        digest_value: str | None = None,
        consume: bool = False,
        stored_status: RequestStatus | None = None,
    ) -> tuple[Decision, list[str], list[str], RequestStatus, list[RequestStatus]]:
        if transitions[-1] != status:
            transitions.append(status)
        self.request_status[key] = stored_status or status
        if digest_value is not None:
            self.request_digests[key] = digest_value
        return decision, reasons, violations, status, transitions

    @staticmethod
    def _agent_stack_violations(contract: PAACContract, request: ActionRequest) -> tuple[str, str] | None:
        if request.agent_stack.agent_id != contract.agent_id:
            return "agent_identity_mismatch", "agent_mismatch"
        if request.agent_stack.agent_version != contract.agent_version:
            return "agent_version_mismatch", "agent_version_mismatch"
        if request.agent_stack.model_id != contract.model_id:
            return "model_identity_mismatch", "model_mismatch"
        undeclared_tools = set(request.agent_stack.tool_ids) - set(contract.declared_tools)
        if undeclared_tools:
            return "undeclared_tool_requested", "undeclared_tools"
        if request.agent_stack.delegated_by and contract.delegation_policy == "none":
            return "delegation_not_declared", "undeclared_delegation"
        return None

    def _now(self) -> datetime:
        when = self.clock()
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        return when.astimezone(timezone.utc)
