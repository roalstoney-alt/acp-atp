from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .core import EnforcementEngine
from .evidence import request_digest
from .fixtures import alpha_contracts
from .models import ActionRequest, ConfirmationRecord


def make_request(contract_id: str, agent_id: str, action_type: str, resource: str, params: dict) -> ActionRequest:
    tool_id = action_type.split(".")[0] + ".mock"
    return ActionRequest(
        request_id=f"req_{contract_id}_{action_type.replace('.', '_')}_{len(str(sorted(params.items())))}",
        contract_id=contract_id,
        agent_id=agent_id,
        action_type=action_type,
        resource=resource,
        params=params,
        created_at=datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc),
        metadata={
            "agent_version": "0.1",
            "model_id": "model.mock.safe",
            "tool_id": tool_id,
        },
    )


def run_demo() -> list[dict]:
    engine = EnforcementEngine(alpha_contracts(), now=datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc))
    requests = [
        make_request("paac_email_demo", "email-agent.mock", "email.draft", "mailbox", {"recipients": ["alice@example.com"], "content_hash": "sha256:demo"}),
        make_request("paac_email_demo", "email-agent.mock", "email.send", "mailbox", {"recipients": ["alice@example.com"], "content_hash": "sha256:demo"}),
        make_request("paac_travel_demo", "travel-agent.mock", "travel.search", "travel_api", {"origin": "SFO", "destination": "YVR"}),
        make_request("paac_travel_demo", "travel-agent.mock", "travel.purchase", "travel_api", {"amount": 620, "currency": "USD"}),
        make_request("paac_file_demo", "file-agent.mock", "file.rename", "/workspace/demo/a.txt", {"path": "/workspace/demo/a.txt"}),
        make_request("paac_file_demo", "file-agent.mock", "file.delete", "/workspace/demo/a.txt", {"path": "/workspace/demo/a.txt"}),
        make_request("paac_file_demo", "file-agent.mock", "file.upload", "/workspace/demo/a.txt", {"path": "/workspace/demo/a.txt"}),
    ]
    return [engine.evaluate(request) for request in requests]


def confirmed_request_result() -> dict:
    now = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)
    request = make_request(
        "paac_email_demo",
        "email-agent.mock",
        "email.send",
        "mailbox",
        {"recipients": ["alice@example.com"], "content_hash": "sha256:demo-confirmed"},
    )
    request = ActionRequest(
        **{**request.__dict__, "metadata": {**request.metadata, "confirmation_nonce": "nonce-demo-001"}}
    )
    confirmations = {
        request.request_id: ConfirmationRecord(
            request_id=request.request_id,
            contract_id=request.contract_id,
            request_digest=request_digest(request),
            nonce="nonce-demo-001",
            confirmed=True,
            confirmed_by="user",
            confirmed_at=now,
            expires_at=now + timedelta(minutes=5),
        )
    }
    return EnforcementEngine(alpha_contracts(), confirmations=confirmations, now=now).evaluate(request)


if __name__ == "__main__":
    for result in run_demo():
        print(result["decision"], ",".join(result["reasons"]))
