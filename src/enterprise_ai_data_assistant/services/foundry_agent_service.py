import json

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from enterprise_ai_data_assistant.services.sql_agent_tools import (
    query_enterprise_database,
)


class FoundryAgentService:
    def __init__(
        self,
        endpoint: str,
        agent_name: str,
        agent_version: str,
    ):
        self.agent_name = agent_name
        self.agent_version = agent_version

        self.project_client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(),
        )

        self.openai_client = self.project_client.get_openai_client()

    def ask_rag_agent(self, question: str) -> str:
        response = self.openai_client.responses.create(
            input=question,
            extra_body={
                "agent_reference": {
                    "name": self.agent_name,
                    "version": self.agent_version,
                    "type": "agent_reference",
                }
            },
        )

        return response.output_text

    def ask_sql_agent(self, question: str) -> str:
        response = self.openai_client.responses.create(
            input=question,
            extra_body={
                "agent_reference": {
                    "name": self.agent_name,
                    "version": self.agent_version,
                    "type": "agent_reference",
                }
            },
        )

        tool_outputs = []

        for item in response.output:
            if item.type == "function_call":
                arguments = json.loads(item.arguments)

                if item.name == "query_enterprise_database":
                    result = query_enterprise_database(question=arguments["question"])

                    tool_outputs.append(
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": json.dumps(result),
                        }
                    )

        if not tool_outputs:
            return response.output_text

        final_response = self.openai_client.responses.create(
            previous_response_id=response.id,
            input=tool_outputs,
            extra_body={
                "agent_reference": {
                    "name": self.agent_name,
                    "version": self.agent_version,
                    "type": "agent_reference",
                }
            },
        )

        return final_response.output_text
