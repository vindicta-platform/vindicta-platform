"""Chainlit entrypoint for the Vindicta Swarm review UI.

Run with::

    chainlit run src/vindicta_agents/ui/chainlit_app.py -w

This module wires Chainlit's human-in-the-loop widgets to the
LangGraph interrupt points, providing:
- Spec review (approve/decline with reason)
- Plan review (approve/decline before execution)
- PR merge approval
"""

from __future__ import annotations


try:
    import chainlit as cl

    CHAINLIT_AVAILABLE = True
except ImportError:
    CHAINLIT_AVAILABLE = False

from vindicta_agents.swarm.review_gates import (
    ReviewAction,
    ReviewBackend,
    ReviewDecision,
)


class ChainlitReviewBackend(ReviewBackend):
    """Chainlit-based review backend using AskActionMessage."""

    async def ask_decision(
        self, title: str, content: str, gate_type: str
    ) -> ReviewDecision:
        if not CHAINLIT_AVAILABLE:
            raise RuntimeError(
                "Chainlit is not installed. Install with: pip install chainlit"
            )

        # Show the content to the reviewer
        await cl.Message(
            content=f"## {title}\n\n{content}",
        ).send()

        # Ask for approve/decline
        actions = [
            cl.Action(name="approve", payload={"value": "approve"}, label="✅ Approve"),
            cl.Action(name="decline", payload={"value": "decline"}, label="❌ Decline"),
        ]

        res = await cl.AskActionMessage(
            content=f"**Review Gate: {gate_type}**\n\nPlease review the above and choose an action:",
            actions=actions,
        ).send()

        if res is None or res.get("payload", {}).get("value") == "approve":
            return ReviewDecision(
                action=ReviewAction.APPROVE,
                reviewer="human",
            )

        # Declined — ask for reason
        reason_res = await cl.AskUserMessage(
            content="Please provide a reason for declining:",
            timeout=300,
        ).send()

        reason = (
            reason_res.get("output", "No reason provided")
            if reason_res
            else "No reason provided"
        )

        return ReviewDecision(
            action=ReviewAction.DECLINE,
            reason=reason,
            reviewer="human",
        )


# ── Chainlit event handlers ────────────────────────────────────────

if CHAINLIT_AVAILABLE:

    @cl.on_chat_start
    async def on_chat_start():
        """Initialize the swarm session."""
        await cl.Message(
            content=(
                "# 🐝 Vindicta Swarm\n\n"
                "Welcome to the autonomous development pipeline.\n\n"
                "Send a feature description to start the SDD lifecycle.\n"
                "You'll be asked to review specs, plans, and PRs at key checkpoints."
            ),
        ).send()

    @cl.on_message
    async def on_message(message: cl.Message):
        """Handle user messages — start the swarm pipeline."""
        from vindicta_agents.swarm.config import MockLLMProvider
        from vindicta_agents.swarm.meta_graph import (
            product_owner_node,
            architect_node,
            adl_node,
        )

        intent = message.content

        # Build initial state
        state = {
            "intent": intent,
            "sdd_stage": "",
            "feature_name": "",
            "branch_name": "",
            "spec_dir": "",
            "spec_content": None,
            "plan_content": None,
            "tasks_content": None,
            "tasks": [],
            "pr_url": None,
            "issue_urls": [],
            "spec_queue": [],
            "decline_memory": [],
            "current_phase": "",
            "error_log": None,
            "execution_log": [],
        }

        config = {"configurable": {"llm_provider": MockLLMProvider()}}

        # Run PO
        await cl.Message(content="🏭 **PO**: Generating spec...").send()
        po_result = product_owner_node(state, config)
        state.update(po_result)

        # Spec review gate
        backend = ChainlitReviewBackend()
        from vindicta_agents.swarm.review_gates import ReviewGate

        spec_gate = ReviewGate(backend=backend, gate_type="spec_review")
        decision = await spec_gate.review(
            title=f"Spec: {state.get('feature_name', 'feature')}",
            content=state.get("spec_content", ""),
        )

        if not decision.approved:
            from vindicta_agents.swarm.spec_queue import DeclineRecord

            state.setdefault("decline_memory", []).append(
                DeclineRecord(
                    feature_name=state.get("feature_name", ""),
                    reason=decision.reason,
                )
            )
            await cl.Message(
                content=f"❌ Spec declined: {decision.reason}\n\nPO will regenerate with this feedback."
            ).send()
            return

        # Run Architect
        await cl.Message(content="🏛️ **Architect**: Creating plan...").send()
        arch_result = architect_node(state, config)
        state.update(arch_result)

        # Run ADL
        await cl.Message(content="📋 **ADL**: Generating tasks...").send()
        adl_result = adl_node(state, config)
        state.update(adl_result)

        # Plan review gate
        plan_gate = ReviewGate(backend=backend, gate_type="plan_review")
        plan_decision = await plan_gate.review(
            title="Implementation Plan",
            content=state.get("plan_content", ""),
        )

        if not plan_decision.approved:
            await cl.Message(content=f"❌ Plan declined: {plan_decision.reason}").send()
            return

        # Execution phase would follow...
        task_count = len(state.get("tasks", []))
        await cl.Message(
            content=(
                f"✅ Plan approved! {task_count} tasks ready for execution.\n\n"
                "Domain agents would now execute tasks, "
                "followed by SD Review → SSE → SM Merge."
            ),
        ).send()
