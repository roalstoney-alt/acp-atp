from __future__ import annotations

from datetime import datetime, timezone

from .models import PAACContract


def dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def alpha_contracts() -> dict[str, PAACContract]:
    start = dt("2026-07-21T00:00:00Z")
    end = dt("2026-07-28T00:00:00Z")
    return {
        "paac_email_demo": PAACContract(
            paac_version="0.1",
            contract_id="paac_email_demo",
            principal_id="user_local_001",
            agent_id="email-agent.mock",
            agent_version="0.1",
            model_id="model.mock.safe",
            tool_ids=["email.mock"],
            purpose="Draft email and send only after confirmation to approved recipients.",
            permitted_actions=["email.draft", "email.send"],
            prohibited_actions=["email.export_contacts", "email.read_unrelated"],
            resources={"email_allowed_recipient_domains": ["example.com"], "allowed_delegated_agent_ids": []},
            constraints={"max_execution_count": 20},
            valid_from=start,
            valid_until=end,
            confirmation_required_actions=["email.send"],
            log_required_actions=["email.draft", "email.send"],
        ),
        "paac_travel_demo": PAACContract(
            paac_version="0.1",
            contract_id="paac_travel_demo",
            principal_id="user_local_001",
            agent_id="travel-agent.mock",
            agent_version="0.1",
            model_id="model.mock.safe",
            tool_ids=["travel.mock"],
            purpose="Search travel and request confirmation before bounded purchase.",
            permitted_actions=["travel.search", "travel.reserve", "travel.purchase"],
            prohibited_actions=["travel.save_payment_credential", "travel.buy_insurance"],
            resources={"travel_allowed_regions": ["US", "CA"], "allowed_delegated_agent_ids": []},
            constraints={"max_payment_amount": 500.0, "allowed_currencies": ["USD"], "max_execution_count": 20},
            valid_from=start,
            valid_until=end,
            confirmation_required_actions=["travel.purchase"],
            log_required_actions=["travel.reserve", "travel.purchase"],
        ),
        "paac_file_demo": PAACContract(
            paac_version="0.1",
            contract_id="paac_file_demo",
            principal_id="user_local_001",
            agent_id="file-agent.mock",
            agent_version="0.1",
            model_id="model.mock.safe",
            tool_ids=["file.mock"],
            purpose="Manage files in a synthetic project folder without deletion or upload.",
            permitted_actions=["file.list", "file.move", "file.rename"],
            prohibited_actions=["file.delete", "file.upload"],
            resources={"file_allowed_paths": ["/workspace/demo"], "allowed_delegated_agent_ids": []},
            constraints={"max_execution_count": 20},
            valid_from=start,
            valid_until=end,
            confirmation_required_actions=[],
            log_required_actions=["file.move", "file.rename"],
        ),
    }
