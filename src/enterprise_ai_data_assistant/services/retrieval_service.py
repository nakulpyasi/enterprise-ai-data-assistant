from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from enterprise_ai_data_assistant.config import settings
from azure.search.documents.models import VectorizableTextQuery

search_client = SearchClient(
    endpoint=settings.azure_search_endpoint,
    index_name=settings.azure_search_index,
    credential=AzureKeyCredential(settings.azure_search_key),
)


def retrieve_chunks(question: str, top_k: int = 3):
    vector_query = VectorizableTextQuery(
        text=question,
        k_nearest_neighbors=top_k,
        fields="text_vector",
    )

    results = search_client.search(
        search_text=question,
        vector_queries=[vector_query],
        select=["chunk_id", "title", "chunk"],
        top=top_k,
    )

    return [
        {
            "chunk_id": result["chunk_id"],
            "title": result["title"],
            "chunk": result["chunk"],
        }
        for result in results
    ]
