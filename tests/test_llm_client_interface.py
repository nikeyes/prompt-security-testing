def test_llm_client_is_abstract():
    from src.helpers.llm_client import LLMClient
    
    try:
        LLMClient()
        assert False, "Should not be able to instantiate abstract class"
    except TypeError:
        pass


def test_bedrock_invoke_client_rejects_nova_models():
    import pytest
    from src.helpers.bedrock_client_invoke import BedrockInvokeClient
    
    client = BedrockInvokeClient()
    
    with pytest.raises(ValueError, match="BedrockInvokeClient only supports Anthropic models"):
        client.invoke_model(
            model_id='eu.amazon.nova-lite-v1:0',
            system_prompt='Test',
            user_prompt='Test'
        )