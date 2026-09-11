from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
import asyncio

from enterprise_ai_data_assistant.config import settings
from enterprise_ai_data_assistant.services.foundry_agent_service import (
    FoundryAgentService,
)

chat_client = FoundryChatClient(
    project_endpoint=settings.foundry_project_endpoint,
    model=settings.azure_openai_model,
    credential=DefaultAzureCredential(),
)

rag_agent_service = FoundryAgentService(
    endpoint=settings.foundry_project_endpoint,
    agent_name=settings.foundry_rag_agent_name,
    agent_version=settings.foundry_rag_agent_version,
)

sql_agent_service = FoundryAgentService(
    endpoint=settings.foundry_project_endpoint,
    agent_name=settings.foundry_sql_agent_name,
    agent_version=settings.foundry_sql_agent_version,
)

agents_used = []


@tool
async def ask_rag_agent(question: str) -> str:
    """Use the registered RAG Agent for document, warranty, and policy questions."""
    print("TOOL CALLED: ask_rag_agent")

    if "rag_agent" not in agents_used:
        agents_used.append("rag_agent")

    return await asyncio.to_thread(rag_agent_service.ask_rag_agent, question)


@tool
async def ask_sql_agent(question: str) -> str:
    """Use the registered SQL Agent for counts, statuses, and database questions."""
    print("TOOL CALLED: ask_sql_agent")

    if "sql_agent" not in agents_used:
        agents_used.append("sql_agent")
    return await asyncio.to_thread(sql_agent_service.ask_sql_agent, question)


manager = Agent(
    client=chat_client,
    instructions=(
        "You coordinate enterprise data questions. "
        "Use ask_rag_agent for document, warranty, and policy questions. "
        "Use ask_sql_agent for counts, statuses, and database questions. "
        "Use both tools when the question requires information from both sources. "
        "Do not invent enterprise information."
    ),
    name="Enterprise Data Manager",
    tools=[ask_rag_agent, ask_sql_agent],
)


async def orchestrate(question: str) -> dict:
    agents_used.clear()

    result = await manager.run(question)

    return {"answer": result.text, "agents_used": agents_used.copy()}


async def main():
    result = await orchestrate(
        "How many support tickets are there and what does the Acme warranty cover?."
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
