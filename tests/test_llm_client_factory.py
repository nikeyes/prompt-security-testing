def test_factory_creates_invoke_client():
    from src.helpers.llm_client_factory import create_llm_client

    client = create_llm_client('invoke')
    assert client.__class__.__name__ == 'BedrockInvokeClient'


def test_factory_creates_converse_client():
    from src.helpers.llm_client_factory import create_llm_client

    client = create_llm_client('converse')
    assert client.__class__.__name__ == 'BedrockConverseClient'
