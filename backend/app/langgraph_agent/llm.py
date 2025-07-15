from langchain_openai import ChatOpenAI

# Initialize the language model to be used by the agent's nodes.
# By placing this in its own file, we avoid circular import errors.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
