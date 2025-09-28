from helpers.llm_client import LLMClient
from helpers.bedrock_client_invoke import BedrockInvokeClient
from helpers.bedrock_client_converse import BedrockConverseClient


def create_llm_client(client_type: str) -> LLMClient:
    if client_type == 'invoke':
        return BedrockInvokeClient()
    elif client_type == 'converse':
        return BedrockConverseClient()
    raise ValueError(f'Unknown client type: {client_type}')
