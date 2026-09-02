from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool, PromptAgentDefinition
from azure.identity import DefaultAzureCredential
from enterprise_ai_data_assistant.config import settings

project = AIProjectClient(
    endpoint=settings.foundry_project_endpoint, credential=DefaultAzureCredential()
)

sql_tool = FunctionTool(
    name="query_enterprise_database",
    description=(
        "Query the enterprise SQL database to answer questions about "
        "support tickets, statuses, counts, and operational metrics."
    ),
    parameters={
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": (
                    "The user's natural-language question about enterprise data."
                ),
            }
        },
        "required": ["question"],
        "additionalProperties": False,
    },
    strict=True,
)

agent = project.agents.create_version(
    agent_name="enterprise-sql-agent",
    definition=PromptAgentDefinition(
        model="gpt-4.1-mini",
        instructions="""
You are an enterprise SQL agent.

For every structured enterprise-data question, always use
query_enterprise_database before answering.

Never invent database values.
Use only the tool result to answer database questions.

After receiving the tool result, provide a concise final answer
and do not call the tool again unless additional data is genuinely required.
""",
        tools=[sql_tool],
    ),
)

print("Agent name: ", agent.name)
print("Agent version: ", agent.version)
