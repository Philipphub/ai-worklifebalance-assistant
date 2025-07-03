from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict

from app.langgraph_agent import nodes


class AgentState(TypedDict):
    """
    Defines the state for our LangGraph agent.
    This is the "memory" of the agent.
    """

    tasks: List[str]
    categorized_tasks: Dict[str, List[str]]
    analysis_report: str


def create_agent_graph():
    """
    Creates the LangGraph agent by defining the state, nodes, and edges.
    """
    # Define the state machine
    workflow = StateGraph(AgentState)

    # Define the nodes
    workflow.add_node("categorize", nodes.categorize_tasks)
    workflow.add_node("analyze", nodes.get_analysis)

    # Define the edges
    workflow.set_entry_point("categorize")
    workflow.add_edge("categorize", "analyze")
    workflow.add_edge("analyze", END)

    # Compile the graph into a runnable agent
    agent = workflow.compile()

    return agent


# Create a single instance of the agent to be used by the application
agent = create_agent_graph()
