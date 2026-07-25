from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable

from trust_layer.core import EnforcementEngine
from trust_layer.models import ActionRequest


@dataclass(frozen=True)
class ToolCall:
    request_id: str
    contract_id: str
    agent_id: str
    agent_version: str
    model_id: str
    tool_id: str
    action_type: str
    resource: str
    params: dict[str, Any]
    created_at: datetime | None = None


class PATLToolAdapter:
    """Isolated authorization wrapper for a LangChain-style tool call boundary."""

    def __init__(self, engine: EnforcementEngine, tools: dict[str, Callable[[dict[str, Any]], Any]]) -> None:
        self.engine = engine
        self.tools = tools

    def invoke(self, call: ToolCall) -> dict[str, Any]:
        patl_metadata = dict(call.params.get("_patl_metadata", {}))
        tool_params = {key: value for key, value in call.params.items() if key != "_patl_metadata"}
        request = ActionRequest(
            request_id=call.request_id,
            contract_id=call.contract_id,
            agent_id=call.agent_id,
            action_type=call.action_type,
            resource=call.resource,
            params=tool_params,
            created_at=call.created_at or datetime.now(timezone.utc),
            metadata={
                "agent_version": call.agent_version,
                "model_id": call.model_id,
                "tool_id": call.tool_id,
                **patl_metadata,
            },
        )
        result = self.engine.evaluate(request)
        if result["decision"] in {"BLOCK", "REQUIRE_CONFIRMATION"}:
            return {"executed": False, "patl": result, "tool_result": None}
        tool = self.tools.get(call.tool_id)
        if tool is None:
            return {"executed": False, "patl": result, "tool_result": None, "adapter_error": "tool_not_registered"}
        return {"executed": True, "patl": result, "tool_result": tool(tool_params)}
