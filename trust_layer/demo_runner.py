from __future__ import annotations

from datetime import datetime, timezone

from .core import EnforcementEngine
from .fixtures import alpha_contracts
from .models import ActionRequest


def make_request(contract_id: str, agent_id: str, action_type: str, resource: str, params: dict) -> ActionRequest:
    return ActionRequest(
        request_id=f"req_{contract_id}_{action_type.replace('.', '_')}_{abs(hash(str(params))) % 100000}",
        contract_id=contract_id,
        agent_id=agent_id,
        action_type=action_type,
        resource=resource,
        params=params,
        created_at=datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc),
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


if __name__ == "__main__":
    for result in run_demo():
        print(result["decision"], ",".join(result["reasons"]))
