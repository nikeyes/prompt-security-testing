from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class LLMClient(ABC):
    @abstractmethod
    def invoke_model(
        self,
        model_id: str,
        system_prompt: str,
        user_prompt: str,
        image_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_client_type(self) -> str:
        pass