from __future__ import annotations

import json
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from trust_layer.core import EnforcementEngine
from trust_layer.evidence import EvidenceLedger, request_digest
from trust_layer.fixtures import alpha_contracts
from trust_layer.models import ActionRequest, ConfirmationRecord, RevocationRegistry


NOW = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)


def req(
    request_id: str,
    contract_id: str,
    agent_id: str,
    action_type: str,
    resource: str,
    params: dict[str, Any],
    metadata: dict[str, Any] | None = None,
    created_at: datetime = NOW,
) -> ActionRequest:
    return ActionRequest(
        request_id=request_id,
        contract_id=contract_id,
        agent_id=agent_id,
        action_type=action_type,
        resource=resource,
        params=params,
        created_at=created_at,
        metadata=metadata
        or {
            "agent_version": "0.1",
            "model_id": "model.mock.safe",
            "tool_id": f"{action_type.split('.')[0]}.mock",
        },
    )


def confirmed(request: ActionRequest, nonce: str = "nonce-bc") -> tuple[ActionRequest, ConfirmationRecord]:
    bound = replace(request, metadata={**request.metadata, "confirmation_nonce": nonce})
    return bound, ConfirmationRecord(
        request_id=bound.request_id,
        contract_id=bound.contract_id,
        request_digest=request_digest(bound),
        nonce=nonce,
        confirmed=True,
        confirmed_by="user",
        confirmed_at=NOW,
        expires_at=NOW + timedelta(minutes=5),
    )


def run_scenarios() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    def record(scenario_id: str, expected: str, observed: str, passed: bool, detail: str = "") -> None:
        results.append({"id": scenario_id, "expected": expected, "observed": observed, "passed": passed, "detail": detail})

    base = alpha_contracts()
    send = req("bc001", "paac_email_demo", "email-agent.mock", "email.send", "mailbox", {"recipients": ["a@example.com"], "content_hash": "sha256:bc"})
    r = EnforcementEngine(alpha_contracts(), now=NOW).evaluate(send)
    record("BC-001", "REQUIRE_CONFIRMATION", r["decision"], r["decision"] == "REQUIRE_CONFIRMATION")

    original, conf = confirmed(send)
    changed = replace(original, request_id="bc002", params={"recipients": ["b@example.com"], "content_hash": "sha256:bc"})
    r = EnforcementEngine(alpha_contracts(), confirmations={"bc002": replace(conf, request_id="bc002")}, now=NOW).evaluate(changed)
    record("BC-002", "REQUIRE_CONFIRMATION", r["decision"], r["decision"] == "REQUIRE_CONFIRMATION")

    purchase = req("bc003", "paac_travel_demo", "travel-agent.mock", "travel.purchase", "travel_api", {"amount": 400, "currency": "USD"})
    original, conf = confirmed(purchase)
    changed = replace(original, params={"amount": 450, "currency": "USD"})
    r = EnforcementEngine(alpha_contracts(), confirmations={"bc003": conf}, now=NOW).evaluate(changed)
    record("BC-003", "REQUIRE_CONFIRMATION", r["decision"], r["decision"] == "REQUIRE_CONFIRMATION")

    r = EnforcementEngine(alpha_contracts(), now=NOW).evaluate(replace(purchase, request_id="bc004", params={"amount": 400, "currency": "CAD"}))
    record("BC-004", "BLOCK", r["decision"], r["decision"] == "BLOCK")

    r = EnforcementEngine(alpha_contracts(), now=NOW).evaluate(replace(send, request_id="bc005", metadata={**send.metadata, "tool_id": "shell.mock"}))
    record("BC-005", "BLOCK", r["decision"], r["decision"] == "BLOCK")

    r = EnforcementEngine(alpha_contracts(), now=NOW).evaluate(replace(send, request_id="bc006", metadata={**send.metadata, "model_id": "model.mock.other"}))
    record("BC-006", "BLOCK", r["decision"], r["decision"] == "BLOCK")

    r = EnforcementEngine(alpha_contracts(), now=NOW).evaluate(replace(send, request_id="bc007", metadata={**send.metadata, "delegated_agent_id": "delegate.mock"}))
    record("BC-007", "BLOCK", r["decision"], r["decision"] == "BLOCK")

    revocations = RevocationRegistry()
    revocations.revoke_contract("paac_email_demo")
    r = EnforcementEngine(alpha_contracts(), revocations=revocations, now=NOW).evaluate(replace(send, request_id="bc008"))
    record("BC-008", "BLOCK", r["decision"], r["decision"] == "BLOCK")

    engine = EnforcementEngine(alpha_contracts(), now=NOW)
    draft = req("bc009", "paac_email_demo", "email-agent.mock", "email.draft", "mailbox", {"recipients": ["a@example.com"], "content_hash": "sha256:bc"})
    first = engine.evaluate(draft)
    second = engine.evaluate(draft)
    record("BC-009", "BLOCK", second["decision"], first["decision"] == "ALLOW_WITH_LOG" and second["decision"] == "BLOCK")

    exhausted_contracts = alpha_contracts()
    exhausted_contracts["paac_email_demo"].constraints["max_execution_count"] = 1
    engine = EnforcementEngine(exhausted_contracts, now=NOW)
    engine.evaluate(replace(draft, request_id="bc010a"))
    r = engine.evaluate(replace(draft, request_id="bc010b"))
    record("BC-010", "BLOCK", r["decision"], r["decision"] == "BLOCK")

    upload = req("bc011", "paac_file_demo", "file-agent.mock", "file.upload", "/workspace/demo/a.txt", {"path": "/workspace/demo/a.txt"})
    r = EnforcementEngine(alpha_contracts(), now=NOW).evaluate(upload)
    record("BC-011", "BLOCK", r["decision"], r["decision"] == "BLOCK")

    escaped = req("bc012", "paac_file_demo", "file-agent.mock", "file.rename", "/etc/passwd", {"path": "/etc/passwd"})
    r = EnforcementEngine(alpha_contracts(), now=NOW).evaluate(escaped)
    record("BC-012", "BLOCK", r["decision"], r["decision"] == "BLOCK")

    ledger = EvidenceLedger()
    EnforcementEngine(alpha_contracts(), ledger=ledger, now=NOW).evaluate(replace(draft, request_id="bc013"))
    ledger.events[0]["decision"] = "ALLOW"
    record("BC-013", "INTEGRITY_FAILURE", "INTEGRITY_FAILURE" if not ledger.verify_integrity() else "OK", not ledger.verify_integrity())

    search = req("bc014", "paac_travel_demo", "travel-agent.mock", "travel.search", "travel_api", {"origin": "SFO", "destination": "YVR"})
    r = EnforcementEngine(alpha_contracts(), now=NOW).evaluate(search)
    record("BC-014", "ALLOW", r["decision"], r["decision"] == "ALLOW")

    exact, conf = confirmed(replace(purchase, request_id="bc015"))
    r = EnforcementEngine(alpha_contracts(), confirmations={"bc015": conf}, now=NOW).evaluate(exact)
    record("BC-015", "ALLOW_WITH_LOG", r["decision"], r["decision"] == "ALLOW_WITH_LOG")

    return results


def main() -> int:
    results = run_scenarios()
    payload = {
        "challenge_id": "PATL-BOUNDARY-CHALLENGE-001",
        "environment": "local synthetic fixtures only",
        "results": results,
        "passed": sum(1 for item in results if item["passed"]),
        "failed": sum(1 for item in results if not item["passed"]),
    }
    output = Path("challenge/BASELINE_RESULTS.json")
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
