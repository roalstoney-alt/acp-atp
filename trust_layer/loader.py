from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from .fixtures import dt
from .models import AgentStack, PAACContract


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PAAC_SCHEMA = REPO_ROOT / "schemas" / "paac-v0.1.schema.json"


class PAACValidationError(ValueError):
    pass


def load_paac_file(path: str | Path, schema_path: str | Path | None = None) -> PAACContract:
    return load_paac_contract(json.loads(Path(path).read_text()), schema_path=schema_path)


def load_paac_contract(data: dict[str, Any], schema_path: str | Path | None = None) -> PAACContract:
    schema = json.loads(Path(schema_path or DEFAULT_PAAC_SCHEMA).read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(data), key=lambda error: list(error.path))
    if errors:
        messages = "; ".join(error.message for error in errors)
        raise PAACValidationError(f"PAAC schema validation failed: {messages}")

    _semantic_validate(data)
    return _construct_contract(data)


def _semantic_validate(data: dict[str, Any]) -> None:
    permitted = set(data["permitted_actions"])
    prohibited = set(data["prohibited_actions"])
    overlap = permitted & prohibited
    if overlap:
        raise PAACValidationError(f"Actions cannot be both permitted and prohibited: {sorted(overlap)}")

    valid_from = dt(data["validity"]["valid_from"])
    valid_until = dt(data["validity"]["valid_until"])
    if valid_from >= valid_until:
        raise PAACValidationError("valid_from must be before valid_until")

    confirmation_actions = set(data.get("confirmation_required_actions", []))
    if not confirmation_actions <= permitted:
        missing = sorted(confirmation_actions - permitted)
        raise PAACValidationError(f"confirmation_required_actions must be permitted first: {missing}")

    log_actions = set(data.get("log_required_actions", []))
    if not log_actions <= permitted:
        missing = sorted(log_actions - permitted)
        raise PAACValidationError(f"log_required_actions must be permitted first: {missing}")

    revocation = data.get("revocation", {})
    if revocation.get("revoked_at") and not revocation.get("revoked"):
        raise PAACValidationError("revoked_at requires revoked=true")


def _construct_contract(data: dict[str, Any]) -> PAACContract:
    agent_stack = data["agent_stack"]
    revocation = data.get("revocation", {})
    return PAACContract(
        paac_version=data["paac_version"],
        contract_id=data["contract_id"],
        principal_id=data["principal"]["pseudonymous_id"],
        agent_stack=AgentStack(
            agent_id=agent_stack["agent_id"],
            agent_version=agent_stack["agent_version"],
            model_id=agent_stack["model_id"],
            tool_ids=tuple(agent_stack.get("tool_ids", [])),
        ),
        purpose=data["purpose"],
        permitted_actions=list(data["permitted_actions"]),
        prohibited_actions=list(data["prohibited_actions"]),
        resources=dict(data["resources"]),
        constraints=dict(data["constraints"]),
        valid_from=dt(data["validity"]["valid_from"]),
        valid_until=dt(data["validity"]["valid_until"]),
        confirmation_required_actions=list(data.get("confirmation_required_actions", [])),
        log_required_actions=list(data.get("log_required_actions", [])),
        maximum_executions=int(data["maximum_executions"]),
        delegation_policy=data["delegation_policy"],
        revoked=bool(revocation.get("revoked", False)),
        revoked_at=dt(revocation["revoked_at"]) if revocation.get("revoked_at") else None,
    )
