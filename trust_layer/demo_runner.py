from __future__ import annotations

from datetime import datetime, timezone

from .core import EnforcementEngine
from .fixtures import public_demo_contracts
from .models import ActionRequest, AgentStack


AGENT_STACKS = {
    "paac_email_demo": AgentStack(
        agent_id="email-agent.mock",
        agent_version="0.1.1",
        model_id="mock-llm-email-v1",
        tool_ids=("mock_email_draft", "mock_email_send"),
    ),
    "paac_travel_demo": AgentStack(
        agent_id="travel-agent.mock",
        agent_version="0.1.1",
        model_id="mock-llm-travel-v1",
        tool_ids=("mock_travel_search", "mock_travel_reserve", "mock_travel_purchase"),
    ),
    "paac_file_demo": AgentStack(
        agent_id="file-agent.mock",
        agent_version="0.1.1",
        model_id="mock-llm-file-v1",
        tool_ids=("mock_file_list", "mock_file_move", "mock_file_rename"),
    ),
}


def make_request(contract_id: str, action_type: str, resource: str, params: dict) -> ActionRequest:
    return ActionRequest(
        request_id=f"req_{contract_id}_{action_type.replace('.', '_')}_{abs(hash(str(params))) % 100000}",
        contract_id=contract_id,
        agent_stack=AGENT_STACKS[contract_id],
        action_type=action_type,
        resource=resource,
        params=params,
        created_at=datetime.now(timezone.utc),
    )


def run_demo() -> list[dict]:
    engine = EnforcementEngine(public_demo_contracts())
    requests = [
        make_request("paac_email_demo", "email.draft", "mailbox", {"recipients": ["alice@example.com"], "content_hash": "sha256:demo"}),
        make_request("paac_email_demo", "email.send", "mailbox", {"recipients": ["alice@example.com"], "content_hash": "sha256:demo"}),
        make_request("paac_travel_demo", "travel.search", "travel_api", {"origin": "SFO", "destination": "YVR"}),
        make_request("paac_travel_demo", "travel.purchase", "travel_api", {"amount": 620, "currency": "USD"}),
        make_request("paac_file_demo", "file.rename", "/workspace/demo/a.txt", {"path": "/workspace/demo/a.txt"}),
        make_request("paac_file_demo", "file.delete", "/workspace/demo/a.txt", {"path": "/workspace/demo/a.txt"}),
        make_request("paac_file_demo", "file.upload", "/workspace/demo/a.txt", {"path": "/workspace/demo/a.txt"}),
    ]
    return [engine.evaluate(request) for request in requests]


if __name__ == "__main__":
    for result in run_demo():
        print(result["decision"], ",".join(result["reasons"]))
