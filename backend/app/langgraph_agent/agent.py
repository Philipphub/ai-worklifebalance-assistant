from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
import json
from app.langgraph_agent.schemas import CategorizedTasks, AnalysisResult, EnhancedAnalysisResult, PriorityRebalanceResult
from app.langgraph_agent.llm import llm
from langchain_core.prompts import ChatPromptTemplate
from app.langgraph_agent.utils import pretty_print

# --- Prompts ---

categorization_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert at categorizing tasks. Your goal is to sort a list of tasks into relevant categories like 'Work', 'Personal', 'Health', and 'Chores'. "
            "Your final output should be a JSON object with a single key 'categorized_tasks' which contains the dictionary of categories.",
        ),
        ("human", "Please categorize the following tasks:\n\n{tasks}"),
    ]
)

analysis_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a work-life balance assistant. Analyze the daily schedule and provide:\n"
            "1. A brief analysis report identifying stress points, lack of breaks, or work-life conflicts\n"
            "2. A stress level (1-10): 1=very relaxed, 10=extremely overwhelming\n"
            "3. Workload assessment: 'light', 'moderate', 'heavy', or 'overwhelming'\n"
            "4. Key concerns (list of main issues)\n"
            "5. Whether the schedule needs rebalancing (true/false)\n\n"
            "Consider factors like: task density, work-life balance, break time, task complexity, and potential conflicts.",
        ),
        (
            "human",
            "Here is the categorized schedule for the day:\n\n{categorized_tasks}\n\nPlease provide your enhanced analysis.",
        ),
    ]
)

priority_rebalance_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert work-life balance coach dealing with a high-stress situation. The user's schedule is overwhelming and needs immediate rebalancing.\n\n"
            "Provide:\n"
            "1. A rebalance report explaining why changes are needed\n"
            "2. Urgent actions to reduce stress immediately\n"
            "3. Tasks that should be rescheduled to another day\n"
            "4. Tasks that could be delegated to others\n"
            "5. Recovery suggestions for stress management\n\n"
            "Be direct but supportive. Focus on practical, actionable solutions.",
        ),
        (
            "human",
            "Based on this analysis:\n\nCategorized Tasks:\n{categorized_tasks}\n\nAnalysis Report:\n{analysis_report}\n\nStress Level: {stress_level}/10\n\nKey Concerns:\n{key_concerns}\n\nPlease provide your priority rebalancing recommendations.",
        ),
    ]
)

suggestion_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful and non-judgmental work-life balance coach. Based on the categorized tasks and the analysis report, generate 2-3 clear, actionable suggestions to help the user improve their day. Focus on protecting personal time and reducing stress.",
        ),
        (
            "human",
            "Given the following information:\n\nCategorized Tasks:\n{categorized_tasks}\n\nAnalysis Report:\n{analysis_report}\n\nPlease provide your suggestions.",
        ),
    ]
)

# --- Agent State ---


class AgentState(TypedDict):
    """
    Defines the state for our LangGraph agent.
    This is the "memory" of the agent.
    """

    tasks: List[str]
    categorized_tasks: Dict[str, List[str]]
    analysis_report: str
    stress_level: int
    workload_assessment: str
    key_concerns: List[str]
    needs_rebalancing: bool
    suggestions: List[str]
    rebalance_report: str
    urgent_actions: List[str]
    tasks_to_reschedule: List[str]
    tasks_to_delegate: List[str]
    recovery_suggestions: List[str]


# --- Nodes ---


def categorize_tasks(state: dict) -> dict:
    """
    Calls an LLM to categorize a list of tasks into a structured format.
    """
    pretty_print("--- Current State before Categorize Node ---", state)
    tasks = state.get("tasks", [])

    # Input sanitization
    if isinstance(tasks, str):
        try:
            tasks = json.loads(tasks)
        except json.JSONDecodeError:
            tasks = [tasks]
    elif isinstance(tasks, list) and len(tasks) == 1 and isinstance(tasks[0], str):
        try:
            tasks = json.loads(tasks[0])
        except (json.JSONDecodeError, TypeError):
            pass

    pretty_print("1. INPUT to Categorize Node", {"tasks": tasks})

    structured_llm = categorization_prompt | llm.with_structured_output(
        CategorizedTasks, method="function_calling"
    )
    response = structured_llm.invoke({"tasks": "\n".join(tasks)})

    pretty_print("1. OUTPUT from Categorize Node", response.dict())
    return {"categorized_tasks": response.categorized_tasks}


def get_analysis(state: dict) -> dict:
    """
    Calls an LLM to analyze the categorized schedule and generate an enhanced report
    with stress level, workload assessment, and rebalancing recommendations.
    """
    pretty_print("--- Current State before Enhanced Analyze Node ---", state)
    categorized_tasks = state.get("categorized_tasks", {})
    pretty_print("2. INPUT to Enhanced Analyze Node", {"categorized_tasks": categorized_tasks})

    structured_llm = analysis_prompt | llm.with_structured_output(
        EnhancedAnalysisResult, method="function_calling"
    )
    response = structured_llm.invoke({"categorized_tasks": categorized_tasks})

    pretty_print("2. OUTPUT from Enhanced Analyze Node", response.dict())
    
    return {
        "analysis_report": response.analysis_report,
        "stress_level": response.stress_level,
        "workload_assessment": response.workload_assessment,
        "key_concerns": response.key_concerns or [],
        "needs_rebalancing": response.needs_rebalancing,
    }


def generate_suggestions(state: dict) -> dict:
    """
    Calls an LLM to generate actionable suggestions based on the analysis.
    """
    pretty_print("--- Current State before Suggestion Node ---", state)
    categorized_tasks = state.get("categorized_tasks", {})
    analysis_report = state.get("analysis_report", "")
    input_data = {
        "categorized_tasks": categorized_tasks,
        "analysis_report": analysis_report,
    }
    pretty_print("3. INPUT to Suggestion Node", input_data)

    structured_llm = suggestion_prompt | llm.with_structured_output(
        AnalysisResult, method="function_calling"
    )
    response = structured_llm.invoke(input_data)

    pretty_print("3. OUTPUT from Suggestion Node", response.dict())
    return {"suggestions": response.suggestions}


def priority_rebalance(state: dict) -> dict:
    """
    Handles high-stress scenarios by providing aggressive rebalancing recommendations.
    This node is triggered when the analysis indicates the schedule needs rebalancing.
    """
    pretty_print("--- Current State before Priority Rebalance Node ---", state)
    
    categorized_tasks = state.get("categorized_tasks", {})
    analysis_report = state.get("analysis_report", "")
    stress_level = state.get("stress_level", 5)
    key_concerns = state.get("key_concerns", [])
    
    input_data = {
        "categorized_tasks": categorized_tasks,
        "analysis_report": analysis_report,
        "stress_level": stress_level,
        "key_concerns": "\n".join(key_concerns) if key_concerns else "No specific concerns identified",
    }
    pretty_print("4. INPUT to Priority Rebalance Node", input_data)

    structured_llm = priority_rebalance_prompt | llm.with_structured_output(
        PriorityRebalanceResult, method="function_calling"
    )
    response = structured_llm.invoke(input_data)

    pretty_print("4. OUTPUT from Priority Rebalance Node", response.dict())
    
    return {
        "rebalance_report": response.rebalance_report,
        "urgent_actions": response.urgent_actions or [],
        "tasks_to_reschedule": response.tasks_to_reschedule or [],
        "tasks_to_delegate": response.tasks_to_delegate or [],
        "recovery_suggestions": response.recovery_suggestions or [],
    }


def should_rebalance(state: dict) -> str:
    """
    Conditional routing function that decides whether to proceed with 
    standard suggestions or priority rebalancing based on the analysis.
    """
    needs_rebalancing = state.get("needs_rebalancing", False)
    stress_level = state.get("stress_level", 5)
    
    pretty_print("--- Conditional Routing Decision ---", {
        "needs_rebalancing": needs_rebalancing,
        "stress_level": stress_level,
    })
    
    # Route to rebalancing if explicitly needed or stress level is high
    if needs_rebalancing or stress_level >= 8:
        return "rebalance"
    else:
        return "suggest"


# --- Graph Definition ---


def create_agent_graph():
    """
    Creates the enhanced LangGraph agent with conditional routing based on stress analysis.
    
    Graph flow:
    1. categorize -> analyze 
    2. analyze -> conditional routing based on stress level/needs_rebalancing
    3a. If high stress: analyze -> rebalance -> END
    3b. If normal stress: analyze -> suggest -> END
    """
    workflow = StateGraph(AgentState)

    # Add all nodes
    workflow.add_node("categorize", categorize_tasks)
    workflow.add_node("analyze", get_analysis)
    workflow.add_node("suggest", generate_suggestions)
    workflow.add_node("rebalance", priority_rebalance)

    # Set entry point
    workflow.set_entry_point("categorize")
    
    # Add static edges
    workflow.add_edge("categorize", "analyze")
    
    # Add conditional routing from analyze node
    workflow.add_conditional_edges(
        "analyze",
        should_rebalance,
        {
            "suggest": "suggest",
            "rebalance": "rebalance",
        }
    )
    
    # Add terminal edges
    workflow.add_edge("suggest", END)
    workflow.add_edge("rebalance", END)

    WorkLifeBalanceAgent = workflow.compile(name="WorkLifeBalanceAgent")
    return WorkLifeBalanceAgent


# --- Agent Instance ---
WorkLifeBalanceAgent = create_agent_graph()
