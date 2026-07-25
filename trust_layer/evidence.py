from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from .models import ActionRequest


def canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def request_digest(request: ActionRequest) -> str:
    return digest(asdict(request))


def build_evidence_event(
    request: ActionRequest,
    decision: str,
    reasons: list[str],
    violations: list[str],
    policy_version: str,
    evaluated_at: datetime,
    previous_event_hash: str = "0" * 64,
) -> dict[str, Any]:
    content_ref = request.params.get("content_ref") or request.params.get("content_hash")
    body = {
        "event_version": "patl-evidence-v0.1",
        "event_type": "patl.enforcement_decision",
        "request_id": request.request_id,
        "contract_id": request.contract_id,
        "agent_id": request.agent_id,
        "action_type": request.action_type,
        "resource": request.resource,
        "decision": decision,
        "reasons": reasons,
        "violations": violations,
        "policy_version": policy_version,
        "created_at": evaluated_at.astimezone(timezone.utc).isoformat(),
        "content_ref": content_ref,
        "request_digest": request_digest(request),
        "previous_event_hash": previous_event_hash,
    }
    body["event_hash"] = digest(body)
    body["event_id"] = "ev_" + body["event_hash"][:24]
    return body


def build_credit_event(evidence: dict[str, Any]) -> dict[str, Any]:
    body = {
        "event_version": "patl-agent-credit-v0.1",
        "event_type": "patl.agent_credit_event",
        "source_evidence_id": evidence["event_id"],
        "agent_id": evidence["agent_id"],
        "contract_id": evidence["contract_id"],
        "action_type": evidence["action_type"],
        "decision": evidence["decision"],
        "violation_count": len(evidence.get("violations", [])),
        "created_at": evidence["created_at"],
    }
    body["event_id"] = "ace_" + digest(body)[:24]
    return body


@dataclass
class EvidenceLedger:
    events: list[dict[str, Any]] | None = None

    def __post_init__(self) -> None:
        self.events = self.events or []

    def append(self, event: dict[str, Any]) -> None:
        self.events.append(event)

    def to_jsonl(self) -> str:
        return "\n".join(canonical_json(event) for event in self.events)

    def last_hash(self) -> str:
        if not self.events:
            return "0" * 64
        return self.events[-1]["event_hash"]

    def verify_integrity(self) -> bool:
        previous = "0" * 64
        for event in self.events:
            if event.get("previous_event_hash") != previous:
                return False
            expected_body = dict(event)
            event_hash = expected_body.pop("event_hash", None)
            event_id = expected_body.pop("event_id", None)
            expected_hash = digest(expected_body)
            if event_hash != expected_hash or event_id != "ev_" + expected_hash[:24]:
                return False
            previous = event_hash
        return True
