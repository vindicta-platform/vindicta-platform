from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .state import VindictaState
from .meta_graph import meta_graph
from .domain_graph import domain_graph
from ..utils.logger import logger


def human_review_node(state: VindictaState):
    # This node acts as a breakpoint so you can review the 'tasks' array before execution.
    logger.info("human_review_phase_initiated", task_count=len(state.get("tasks", [])))
    # Return empty dict to indicate no state changes, or return updated keys.
    # Returning state (full object) can cause issues with state merging in some LangGraph configs.
    return {}


def build_master_graph(interrupt: bool = True):
    master_builder = StateGraph(VindictaState)

    # Add the sub-graphs as nodes
    master_builder.add_node("PlanningPhase", meta_graph)
    master_builder.add_node("HumanReview", human_review_node)
    master_builder.add_node("ExecutionPhase", domain_graph)

    master_builder.set_entry_point("PlanningPhase")
    master_builder.add_edge("PlanningPhase", "HumanReview")
    master_builder.add_edge("HumanReview", "ExecutionPhase")
    master_builder.add_edge("ExecutionPhase", END)

    # Use MemorySaver for development visualization
    memory = MemorySaver()

    # Compile with optional interrupt
    compile_kwargs = {"checkpointer": memory}
    if interrupt:
        compile_kwargs["interrupt_before"] = ["ExecutionPhase"]

    return master_builder.compile(**compile_kwargs)


# Export the compiled swarm instance with default behavior
vindicta_swarm = build_master_graph()
