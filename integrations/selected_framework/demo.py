from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from trust_layer.core import EnforcementEngine
from trust_layer.evidence import request_digest
from trust_layer.fixtures import alpha_contracts
from trust_layer.models import ActionRequest, ConfirmationRecord, RevocationRegistry

from .adapter import PATLToolAdapter, ToolCall


NOW = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)


def mock_travel_tool(params: dict) -> dict:
    return {"ok": True, "query": params}


def mock_email_tool(params: dict) -> dict:
    return {"ok": True, "recipients": params.get("recipients", [])}


def _confirmed_email_call() -> tuple[ToolCall, ConfirmationRecord]:
    call = ToolCall(
        request_id="int-confirmed-send",
        contract_id="paac_email_demo",
        agent_id="email-agent.mock",
        agent_version="0.1",
        model_id="model.mock.safe",
        tool_id="email.mock",
        action_type="email.send",
        resource="mailbox",
        params={
            "recipients": ["alice@example.com"],
            "content_hash": "sha256:integration",
            "_patl_metadata": {"confirmation_nonce": "nonce-int-001"},
        },
        created_at=NOW,
    )
    request = ActionRequest(
        request_id=call.request_id,
        contract_id=call.contract_id,
        agent_id=call.agent_id,
        action_type=call.action_type,
        resource=call.resource,
        params={"recipients": ["alice@example.com"], "content_hash": "sha256:integration"},
        created_at=NOW,
        metadata={
            "agent_version": call.agent_version,
            "model_id": call.model_id,
            "tool_id": call.tool_id,
            "confirmation_nonce": "nonce-int-001",
        },
    )
    confirmation = ConfirmationRecord(
        request_id=request.request_id,
        contract_id=request.contract_id,
        request_digest=request_digest(request),
        nonce="nonce-int-001",
        confirmed=True,
        confirmed_by="user",
        confirmed_at=NOW,
        expires_at=NOW + timedelta(minutes=5),
    )
    return call, confirmation


def run_demo() -> dict:
    engine = EnforcementEngine(alpha_contracts(), now=NOW)
    adapter = PATLToolAdapter(engine, {"travel.mock": mock_travel_tool, "email.mock": mock_email_tool})
    allow = adapter.invoke(ToolCall(
        request_id="int-allow-search",
        contract_id="paac_travel_demo",
        agent_id="travel-agent.mock",
        agent_version="0.1",
        model_id="model.mock.safe",
        tool_id="travel.mock",
        action_type="travel.search",
        resource="travel_api",
        params={"origin": "SFO", "destination": "YVR"},
        created_at=NOW,
    ))
    needs_confirmation = adapter.invoke(ToolCall(
        request_id="int-send-pause",
        contract_id="paac_email_demo",
        agent_id="email-agent.mock",
        agent_version="0.1",
        model_id="model.mock.safe",
        tool_id="email.mock",
        action_type="email.send",
        resource="mailbox",
        params={"recipients": ["alice@example.com"], "content_hash": "sha256:integration"},
        created_at=NOW,
    ))
    confirmed_call, confirmation = _confirmed_email_call()
    engine.confirmations[confirmation.request_id] = confirmation
    confirmed = adapter.invoke(confirmed_call)

    revocations = RevocationRegistry()
    revocations.revoke_contract("paac_travel_demo")
    revoked_adapter = PATLToolAdapter(
        EnforcementEngine(alpha_contracts(), revocations=revocations, now=NOW),
        {"travel.mock": mock_travel_tool},
    )
    revoked = revoked_adapter.invoke(ToolCall(
        request_id="int-revoked-search",
        contract_id="paac_travel_demo",
        agent_id="travel-agent.mock",
        agent_version="0.1",
        model_id="model.mock.safe",
        tool_id="travel.mock",
        action_type="travel.search",
        resource="travel_api",
        params={"origin": "SFO", "destination": "YVR"},
        created_at=NOW,
    ))
    undeclared_tool = adapter.invoke(ToolCall(
        request_id="int-shell",
        contract_id="paac_email_demo",
        agent_id="email-agent.mock",
        agent_version="0.1",
        model_id="model.mock.safe",
        tool_id="shell.mock",
        action_type="email.draft",
        resource="mailbox",
        params={"recipients": ["alice@example.com"], "content_hash": "sha256:integration"},
        created_at=NOW,
    ))
    return {
        "framework_boundary": "LangChain-style tool invocation wrapper",
        "framework_dependency_installed": False,
        "allow": allow["patl"]["decision"],
        "confirmation_pause": needs_confirmation["patl"]["decision"],
        "confirmed": confirmed["patl"]["decision"],
        "revoked": revoked["patl"]["decision"],
        "undeclared_tool": undeclared_tool["patl"]["decision"],
        "evidence_integrity": engine.ledger.verify_integrity(),
    }


if __name__ == "__main__":
    print(json.dumps(run_demo(), indent=2, sort_keys=True))
