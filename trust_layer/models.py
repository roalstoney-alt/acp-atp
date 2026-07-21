from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class RequestStatus(str, Enum):
    PENDING = "PENDING"
    AWAITING_CONFIRMATION = "AWAITING_CONFIRMATION"
    AUTHORIZED = "AUTHORIZED"
    EXECUTED = "EXECUTED"
    CONSUMED = "CONSUMED"
    BLOCKED = "BLOCKED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"


@dataclass(frozen=True)
class AgentStack:
    agent_id: str
    agent_version: str
    model_id: str
    tool_ids: tuple[str, ...] = ()
    delegated_by: str | None = None

    def normalized(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_version": self.agent_version,
            "model_id": self.model_id,
            "tool_ids": sorted(self.tool_ids),
            "delegated_by": self.delegated_by,
        }


@dataclass
class PAACContract:
    paac_version: str
    contract_id: str
    principal_id: str
    agent_stack: AgentStack
    purpose: str
    permitted_actions: list[str]
    prohibited_actions: list[str]
    resources: dict[str, Any]
    constraints: dict[str, Any]
    valid_from: datetime
    valid_until: datetime
    confirmation_required_actions: list[str] = field(default_factory=list)
    log_required_actions: list[str] = field(default_factory=list)
    maximum_executions: int = 1
    delegation_policy: str = "none"
    revoked: bool = False
    revoked_at: datetime | None = None
    execution_count: int = 0

    @property
    def agent_id(self) -> str:
        return self.agent_stack.agent_id

    @property
    def agent_version(self) -> str:
        return self.agent_stack.agent_version

    @property
    def model_id(self) -> str:
        return self.agent_stack.model_id

    @property
    def declared_tools(self) -> tuple[str, ...]:
        return self.agent_stack.tool_ids

    def is_active_at(self, when: datetime) -> bool:
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        return self.valid_from <= when <= self.valid_until and not self.revoked

    def executions_available(self) -> bool:
        return self.execution_count < self.maximum_executions


@dataclass(frozen=True)
class ActionRequest:
    request_id: str
    contract_id: str
    agent_stack: AgentStack
    action_type: str
    resource: str
    params: dict[str, Any]
    created_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def agent_id(self) -> str:
        return self.agent_stack.agent_id


@dataclass(frozen=True)
class ConfirmationRecord:
    request_id: str
    contract_id: str
    confirmed: bool
    confirmed_by: str
    confirmed_at: datetime
    issued_at: datetime
    expires_at: datetime
    nonce: str
    request_digest: str
    signature: str | None = None

    def is_active_at(self, when: datetime) -> bool:
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        return self.issued_at <= when <= self.expires_at


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
