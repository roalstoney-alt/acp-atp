from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .models import AgentStack, PAACContract


def dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def dated_alpha_contracts(
    start: datetime | None = None, end: datetime | None = None
) -> dict[str, PAACContract]:
    """Deterministic fixtures for unit and adversarial tests."""
    start = start or dt("2026-07-21T00:00:00Z")
    end = end or dt("2026-07-28T00:00:00Z")
    return _contracts(start, end)


def public_demo_contracts(clock=None) -> dict[str, PAACContract]:
    """Dynamic fixtures for public local demos so they remain runnable over time."""
    now = clock() if clock else datetime.now(timezone.utc)
    return _contracts(now - timedelta(days=1), now + timedelta(days=7))


def alpha_contracts() -> dict[str, PAACContract]:
    return dated_alpha_contracts()


def _contracts(start: datetime, end: datetime) -> dict[str, PAACContract]:
    return {
        "paac_email_demo": PAACContract(
            paac_version="0.1",
            contract_id="paac_email_demo",
            principal_id="user_local_001",
            agent_stack=AgentStack(
                agent_id="email-agent.mock",
                agent_version="0.1.1",
                model_id="mock-llm-email-v1",
                tool_ids=("mock_email_draft", "mock_email_send"),
            ),
            purpose="Draft email and send only after confirmation to approved recipients.",
            permitted_actions=["email.draft", "email.send"],
            prohibited_actions=["email.export_contacts", "email.read_unrelated"],
            resources={"email_allowed_recipient_domains": ["example.com"]},
            constraints={},
            valid_from=start,
            valid_until=end,
            confirmation_required_actions=["email.send"],
            log_required_actions=["email.draft", "email.send"],
            maximum_executions=20,
            delegation_policy="none",
        ),
        "paac_travel_demo": PAACContract(
            paac_version="0.1",
            contract_id="paac_travel_demo",
            principal_id="user_local_001",
            agent_stack=AgentStack(
                agent_id="travel-agent.mock",
                agent_version="0.1.1",
                model_id="mock-llm-travel-v1",
                tool_ids=("mock_travel_search", "mock_travel_reserve", "mock_travel_purchase"),
            ),
            purpose="Search travel and request confirmation before bounded purchase.",
            permitted_actions=["travel.search", "travel.reserve", "travel.purchase"],
            prohibited_actions=["travel.save_payment_credential", "travel.buy_insurance"],
            resources={"travel_allowed_regions": ["US", "CA"]},
            constraints={"max_payment_amount": 500.0, "allowed_currencies": ["USD"]},
            valid_from=start,
            valid_until=end,
            confirmation_required_actions=["travel.purchase"],
            log_required_actions=["travel.reserve", "travel.purchase"],
            maximum_executions=20,
            delegation_policy="none",
        ),
        "paac_file_demo": PAACContract(
            paac_version="0.1",
            contract_id="paac_file_demo",
            principal_id="user_local_001",
            agent_stack=AgentStack(
                agent_id="file-agent.mock",
                agent_version="0.1.1",
                model_id="mock-llm-file-v1",
                tool_ids=("mock_file_list", "mock_file_move", "mock_file_rename"),
            ),
            purpose="Manage files in a synthetic project folder without deletion or upload.",
            permitted_actions=["file.list", "file.move", "file.rename"],
            prohibited_actions=["file.delete", "file.upload"],
            resources={"file_allowed_paths": ["/workspace/demo"]},
            constraints={},
            valid_from=start,
            valid_until=end,
            confirmation_required_actions=[],
            log_required_actions=["file.move", "file.rename"],
            maximum_executions=20,
            delegation_policy="none",
        ),
    }
