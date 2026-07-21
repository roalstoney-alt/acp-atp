from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

from .models import ActionRequest


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def request_digest(request: ActionRequest) -> str:
    body = {
        "contract_id": request.contract_id,
        "request_id": request.request_id,
        "agent_stack": request.agent_stack.normalized(),
        "action_type": request.action_type,
        "resource": request.resource,
        "params": request.params,
    }
    return digest(body)


def build_evidence_event(
    request: ActionRequest,
    decision: str,
    lifecycle_status: str,
    lifecycle_transitions: list[str],
    request_digest_value: str,
    reasons: list[str],
    violations: list[str],
    policy_version: str,
    evaluated_at: datetime,
) -> dict[str, Any]:
    content_ref = request.params.get("content_ref") or request.params.get("content_hash")
    body = {
        "event_version": "patl-evidence-v0.1.1",
        "event_type": "patl.enforcement_decision",
        "request_id": request.request_id,
        "request_digest": request_digest_value,
        "contract_id": request.contract_id,
        "agent_stack": request.agent_stack.normalized(),
        "agent_id": request.agent_id,
        "action_type": request.action_type,
        "resource": request.resource,
        "decision": decision,
        "lifecycle_status": lifecycle_status,
        "lifecycle_transitions": lifecycle_transitions,
        "reasons": reasons,
        "violations": violations,
        "policy_version": policy_version,
        "created_at": evaluated_at.astimezone(timezone.utc).isoformat(),
        "content_ref": content_ref,
    }
    body["event_id"] = "ev_" + digest(body)[:24]
    return body


def build_credit_event(evidence: dict[str, Any]) -> dict[str, Any]:
    body = {
        "event_version": "patl-agent-credit-v0.1.1",
        "event_type": "patl.agent_credit_event",
        "source_evidence_id": evidence["event_id"],
        "agent_id": evidence["agent_id"],
        "contract_id": evidence["contract_id"],
        "action_type": evidence["action_type"],
        "decision": evidence["decision"],
        "lifecycle_status": evidence["lifecycle_status"],
        "violation_count": len(evidence.get("violations", [])),
        "created_at": evidence["created_at"],
    }
    body["event_id"] = "ace_" + digest(body)[:24]
    return body


@dataclass
class EvidenceLedger:
    ledger_id: str = "patl-local-ledger-v0.1.1"
    clock: Callable[[], datetime] | None = None
    records: list[dict[str, Any]] = field(default_factory=list)

    def _now(self) -> datetime:
        if self.clock:
            return self.clock()
        return datetime.now(timezone.utc)

    @property
    def events(self) -> list[dict[str, Any]]:
        return [record["event"] for record in self.records]

    def append(self, event: dict[str, Any]) -> dict[str, Any]:
        event_copy = deepcopy(event)
        previous_event_hash = self.records[-1]["event_hash"] if self.records else None
        record = {
            "ledger_id": self.ledger_id,
            "sequence": len(self.records) + 1,
            "previous_event_hash": previous_event_hash,
            "event": event_copy,
            "event_hash": digest(event_copy),
            "recorded_at": self._now().astimezone(timezone.utc).isoformat(),
        }
        self.records.append(record)
        return record

    def verify_integrity(self) -> bool:
        previous_hash = None
        for expected_sequence, record in enumerate(self.records, start=1):
            if record.get("ledger_id") != self.ledger_id:
                return False
            if record.get("sequence") != expected_sequence:
                return False
            if record.get("previous_event_hash") != previous_hash:
                return False
            if record.get("event_hash") != digest(record.get("event")):
                return False
            previous_hash = record.get("event_hash")
        return True

    def to_jsonl(self) -> str:
        return "\n".join(canonical_json(record) for record in self.records)
