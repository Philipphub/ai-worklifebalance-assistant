from typing import List


def categorize_tasks(state: dict) -> dict:
    """
    A placeholder node that simulates categorizing tasks.
    In the future, this will call an LLM.
    """
    print("---CATEGORIZING TASKS---")
    tasks = state.get("tasks", [])
    print(f"Input tasks: {tasks}")

    # Simulate LLM categorization
    categorized = {
        "Work": [t for t in tasks if "work" in t.lower()],
        "Personal": [t for t in tasks if "personal" in t.lower()],
    }

    return {"categorized_tasks": categorized}


def get_analysis(state: dict) -> dict:
    """
    A placeholder node that simulates analyzing the schedule.
    In the future, this will call an LLM.
    """
    print("---ANALYZING SCHEDULE---")
    categorized_tasks = state.get("categorized_tasks", {})
    print(f"Input categories: {categorized_tasks}")

    # Simulate LLM analysis
    report = "This is a simulated analysis based on the categorized tasks."

    return {"analysis_report": report}
