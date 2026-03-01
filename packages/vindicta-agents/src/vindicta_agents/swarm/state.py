"""Vindicta Swarm shared state.

``VindictaState`` is a LangGraph TypedDict consumed by every node in
the graph.  It tracks:

- The user intent and routing phase
- SDD lifecycle stage (specify → clarify → plan → tasks → implement → verify → merge)
- Spec queue + decline memory for the autonomous PO loop
- Task execution results (code diffs, issue/PR URLs)
"""

from __future__ import annotations

import operator
from typing import Annotated, List, Optional, TypedDict

from vindicta_agents.swarm.spec_queue import DeclineRecord, SpecQueueItem


class Task(TypedDict):
    """A unit of work assigned to a domain agent."""

    id: str
    description: str
    target_realm: str  # e.g., 'vindicta-engine', 'warscribe-system'
    status: str  # 'pending', 'in-progress', 'completed', 'failed'
    code_diff: Optional[str]  # The actual code written by the Domain Agent


class VindictaState(TypedDict):
    """Full state for the Vindicta Swarm graph.

    This state flows through all nodes (SM → PO → Architect → ADL →
    SD → Domain Agents → SSE → SM Merge).
    """

    # ── Top-Level Context ──
    intent: str

    # ── SDD Lifecycle ──
    sdd_stage: str  # specify, clarify, plan, tasks, implement, verify, merge
    feature_name: str
    branch_name: str
    spec_dir: str  # path to the spec directory

    # ── Artifact Content ──
    spec_content: Optional[str]
    plan_content: Optional[str]
    tasks_content: Optional[str]

    # ── Execution State ──
    tasks: Annotated[List[Task], operator.add]

    # ── Git / GitHub ──
    pr_url: Optional[str]
    issue_urls: Annotated[List[str], operator.add]

    # ── Spec Queue (PO Loop) ──
    spec_queue: List[SpecQueueItem]
    decline_memory: List[DeclineRecord]

    # ── Routing & Control ──
    current_phase: str  # 'planning', 'review', 'execution', 'done'
    error_log: Optional[str]
    execution_log: Annotated[List[str], operator.add]
