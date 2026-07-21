from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class PAACContract:
    paac_version: str
    contract_id: str
    principal_id: str
    agent_id: str
    agent_version: str
    purpose: str
    permitted_actions: list[str]
    prohibited_actions: list[str]
    resources: dict[str, Any]
    constraints: dict[str, Any]
    valid_from: datetime
    valid_until: datetime
    confirmation_required_actions: list[str] = field(default_factory=list)
    log_required_actions: list[str] = field(default_factory=list)
    used_request_ids: set[str] = field(default_factory=set)

    def is_active_at(self, when: datetime) -> bool:
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        return self.valid_from <= when <= self.valid_until


@dataclass(frozen=True)
class ActionRequest:
    request_id: str
    contract_id: str
    agent_id: str
    action_type: str
    resource: str
    params: dict[str, Any]
    created_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ConfirmationRecord:
    request_id: str
    contract_id: str
    confirmed: bool
    confirmed_by: str
    confirmed_at: datetime


@dataclass
class RevocationRegistry:
    revoked_contracts: set[str] = field(default_factory=set)
    revoked_agents: set[str] = field(default_factory=set)

    def revoke_contract(self, contract_id: str) -> None:
        self.revoked_contracts.add(contract_id)

    def revoke_agent(self, agent_id: str) -> None:
        self.revoked_agents.add(agent_id)

    def is_revoked(self, contract_id: str, agent_id: str) -> bool:
        return contract_id in self.revoked_contracts or agent_id in self.revoked_agents
