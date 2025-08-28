def test_llm_client_is_abstract():
    from src.helpers.llm_client import LLMClient
    
    try:
        LLMClient()
        assert False, "Should not be able to instantiate abstract class"
    except TypeError:
        pass