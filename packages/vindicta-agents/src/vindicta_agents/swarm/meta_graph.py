"""Meta-graph: PO → Architect → ADL pipeline.

Each node uses the ``LLMProvider`` from config and the system prompts
from ``swarm.prompts``.  The PO integrates with the spec queue and
decline memory.

This module also contains the generic ``make_planning_node`` factory
used by the JSON-config–driven flow.
"""

from __future__ import annotations

import json
import pathlib
from typing import Any, Dict, Optional, TypedDict, Callable

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, StateGraph

from vindicta_agents.sdk.models import AITask

from .config import MockLLMProvider
from .prompts import ADL_SYSTEM, ARCHITECT_SYSTEM, PO_SYSTEM
from .spec_queue import DeclineMemory
from .state import VindictaState


# ── helpers ──────────────────────────────────────────────────────────


def _provider(config: RunnableConfig):
    return config.get("configurable", {}).get("llm_provider", MockLLMProvider())


# ── PO node ──────────────────────────────────────────────────────────


def product_owner_node(state: VindictaState, config: RunnableConfig):
    """Generate a spec and add it to the spec queue.

    The PO's prompt is augmented with decline memory so it can avoid
    repeating previously rejected patterns.
    """
    provider = _provider(config)

    # Build decline context from state
    decline_records = state.get("decline_memory", [])
    if decline_records:
        dm = DeclineMemory()
        for r in decline_records:
            dm.add(r.feature_name, r.reason, getattr(r, "spec_content", ""))
        decline_context = dm.format_for_prompt()
    else:
        decline_context = "No previous rejections."

    system = PO_SYSTEM.format(decline_context=decline_context)

    task = AITask(
        name="Spec Creation",
        system=system,
        prompt=f"Write a feature spec for: {state['intent']}",
    )
    spec_text = task.execute(provider=provider)

    feature_name = state.get(
        "feature_name", state["intent"][:40].replace(" ", "-").lower()
    )

    return {
        "spec_content": spec_text,
        "sdd_stage": "specify",
        "feature_name": feature_name,
        "current_phase": "planning",
        "execution_log": [f"PO: generated spec for '{feature_name}'"],
    }


# ── Architect node ───────────────────────────────────────────────────


def architect_node(state: VindictaState, config: RunnableConfig):
    """Create an implementation plan from the spec."""
    provider = _provider(config)
    spec = state.get("spec_content", "")

    task = AITask(
        name="Plan Creation",
        system=ARCHITECT_SYSTEM,
        prompt=f"Create an implementation plan for this spec:\n\n{spec}",
    )
    plan_text = task.execute(provider=provider)

    return {
        "plan_content": plan_text,
        "sdd_stage": "plan",
        "execution_log": ["Architect: plan created"],
    }


# ── ADL node ─────────────────────────────────────────────────────────


def adl_node(state: VindictaState, config: RunnableConfig):
    """Break the plan into executable tasks (JSON array)."""
    provider = _provider(config)
    plan = state.get("plan_content", "")

    task = AITask(
        name="Task Slicing",
        system=ADL_SYSTEM,
        prompt=plan,
    )
    tasks_json = task.execute_json(provider=provider)

    return {
        "tasks": tasks_json,
        "tasks_content": str(tasks_json),
        "sdd_stage": "tasks",
        "current_phase": "review",
        "execution_log": [f"ADL: generated {len(tasks_json)} tasks"],
    }


# ── Generic Planning Node Factory (JSON-config driven) ───────────────


class AgentConfig(TypedDict, total=False):
    """Configuration for a planning agent node."""

    task_name: str
    system_prompt: str
    input_key: str
    output_key: str
    prompt_template: str
    phase_update: Optional[str]
    json_mode: bool


_PLANNING_CONFIG_PATH = (
    pathlib.Path(__file__).parent / "configs" / "planning_agents.json"
)


def _load_planning_agents() -> Dict[str, AgentConfig]:
    try:
        with open(_PLANNING_CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


PLANNING_AGENTS: Dict[str, AgentConfig] = _load_planning_agents()


def make_planning_node(
    agent_id: str,
) -> Callable[[VindictaState, RunnableConfig], Dict[str, Any]]:
    """
    Creates a LangGraph node function for a specific planning agent.

    Falls back to the direct node functions (product_owner_node, etc.)
    if PLANNING_AGENTS is empty (no JSON config file).
    """
    config_data = PLANNING_AGENTS.get(agent_id)
    if not config_data:
        # Fallback to the direct implementations
        _fallbacks = {
            "PO": product_owner_node,
            "Architect": architect_node,
            "ADL": adl_node,
        }
        if agent_id in _fallbacks:
            return _fallbacks[agent_id]
        raise ValueError(f"Unknown agent_id: {agent_id}")

    task_name = config_data["task_name"]
    system_prompt = config_data["system_prompt"]
    input_key = config_data["input_key"]
    output_key = config_data["output_key"]
    prompt_template = config_data["prompt_template"]
    phase_update = config_data.get("phase_update")
    json_mode = config_data.get("json_mode", False)

    def planning_node(state: VindictaState, config: RunnableConfig) -> Dict[str, Any]:
        configurable = config.get("configurable", {})
        provider = configurable.get("llm_provider", MockLLMProvider())

        input_value = state.get(input_key, "")  # type: ignore

        task = AITask(
            name=task_name,
            system=system_prompt,
            prompt=prompt_template.format(input=input_value),
        )

        updates: Dict[str, Any] = {}

        if json_mode:
            result_json = task.execute_json(provider=provider)
            updates[output_key] = result_json
        else:
            result_text = task.execute(provider=provider)
            updates[output_key] = result_text

        if phase_update:
            updates["current_phase"] = phase_update

        return updates

    planning_node.__name__ = f"{agent_id.lower()}_node"
    return planning_node


# ── Graph Construction ───────────────────────────────────────────────


def build_meta_graph() -> Any:
    """
    Constructs and compiles the StateGraph for the planning layer.
    """
    meta_builder = StateGraph(VindictaState)

    meta_builder.add_node("PO", product_owner_node)
    meta_builder.add_node("Architect", architect_node)
    meta_builder.add_node("ADL", adl_node)

    meta_builder.set_entry_point("PO")
    meta_builder.add_edge("PO", "Architect")
    meta_builder.add_edge("Architect", "ADL")
    meta_builder.add_edge("ADL", END)

    return meta_builder.compile()


meta_graph = build_meta_graph()
