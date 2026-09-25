import json
from openai import APIConnectionError, APIStatusError, APITimeoutError, RateLimitError
from enterprise_ai_data_assistant.exceptions import (
    FoundryResponseError,
    FoundryTimeoutError,
    FoundryUnavailableError,
)

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
        timeout_seconds: float = 60.0,
        max_retries: int = 2,
    ):
        self.agent_name = agent_name
        self.agent_version = agent_version

        self.project_client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(),
        )

        self.openai_client = self.project_client.get_openai_client(
            timeout=timeout_seconds, max_retries=max_retries
        )

    def _create_response(self, **kwargs):
        """Call Foundry and translate SDK errors into application errors."""

        try:
            # Forward the supplied arguments to the Foundry/OpenAI client.
            return self.openai_client.responses.create(**kwargs)

        except APITimeoutError as error:
            # Convert the SDK timeout into our application's timeout category.
            raise FoundryTimeoutError(
                "Foundry did not respond within the configured timeout"
            ) from error

        except RateLimitError as error:
            # Foundry is reachable but temporarily rejecting excess requests.
            raise FoundryUnavailableError(
                "Foundry is temporarily rate-limited"
            ) from error

        except APIConnectionError as error:
            # The application could not establish or maintain the connection.
            raise FoundryUnavailableError("Could not connect to Foundry") from error

        except APIStatusError as error:
            # Treat temporary Foundry server failures as unavailable.
            if error.status_code >= 500:
                raise FoundryUnavailableError(
                    "Foundry returned a server error"
                ) from error

            # Other unexpected HTTP responses are treated as invalid responses.
            raise FoundryResponseError("Foundry rejected the request") from error

    def _get_output_text(self, response) -> str:
        output_text = response.output_text
        if not isinstance(output_text, str) or not output_text.strip():
            raise FoundryResponseError(
                "Foundry returned an empty or invalid text response"
            )
        return output_text.strip()

    def ask_rag_agent(self, question: str) -> str:
        response = self._create_response(
            input=question,
            extra_body={
                "agent_reference": {
                    "name": self.agent_name,
                    "version": self.agent_version,
                    "type": "agent_reference",
                }
            },
        )

        return self._get_output_text(response)

    def ask_sql_agent(self, question: str) -> str:
        response = self._create_response(
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
            if item.type != "function_call":
                continue

            if item.name != "query_enterprise_database":
                raise FoundryResponseError(
                    f"Foundry requested an unexpected tool: {item.name}"
                )

            try:
                arguments = json.loads(item.arguments)
            except (json.JSONDecodeError, TypeError) as error:
                raise FoundryResponseError(
                    "Foundry returned invalid too-call json"
                ) from error

            tool_question = (
                arguments.get("question") if isinstance(arguments, dict) else None
            )

            if not isinstance(tool_question, str) or not tool_question.strip():
                raise FoundryResponseError(
                    "Foundry returned an invalid database-tool question"
                )

            result = query_enterprise_database(tool_question.strip())

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result, default=str),
                }
            )

        if not tool_outputs:
            return self._get_output_text(response)

        final_response = self._create_response(
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

        return self._get_output_text(final_response)
