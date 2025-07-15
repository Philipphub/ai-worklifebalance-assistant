from typing import List, Dict
from app.langgraph_agent.agent import WorkLifeBalanceAgent


def analyze_schedule_service(tasks: List[str]) -> Dict:
    """
    This service invokes the enhanced LangGraph agent to perform the full
    schedule analysis with stress assessment and conditional rebalancing.
    """
    print("Analysis service: Invoking enhanced LangGraph agent...")

    # The initial state for the agent
    initial_state = {"tasks": tasks}

    # Run the agent and get the final state
    final_state = WorkLifeBalanceAgent.invoke(initial_state)

    print("Analysis service: Agent finished.")

    # Build the response with all possible fields
    response = {
        "categorized_tasks": final_state.get("categorized_tasks", {}),
        "analysis_report": final_state.get("analysis_report", ""),
        "stress_level": final_state.get("stress_level", 5),
        "workload_assessment": final_state.get("workload_assessment", "moderate"),
        "key_concerns": final_state.get("key_concerns", []),
        "needs_rebalancing": final_state.get("needs_rebalancing", False),
    }

    # Add standard suggestions if present (low/moderate stress path)
    if final_state.get("suggestions"):
        response["suggestions"] = final_state.get("suggestions", [])

    # Add rebalancing fields if present (high stress path)
    if final_state.get("rebalance_report"):
        response.update({
            "rebalance_report": final_state.get("rebalance_report"),
            "urgent_actions": final_state.get("urgent_actions", []),
            "tasks_to_reschedule": final_state.get("tasks_to_reschedule", []),
            "tasks_to_delegate": final_state.get("tasks_to_delegate", []),
            "recovery_suggestions": final_state.get("recovery_suggestions", []),
        })

    return response
