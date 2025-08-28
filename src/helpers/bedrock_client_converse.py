import base64
from typing import Optional, Dict, Any

import boto3

from config import (
    AWS_PROFILE,
    AWS_REGION_FRANKFURT,
    MAX_TOKENS,
    TEMPERATURE,
    TOP_K,
    TOP_P,
)
from helpers.llm_client import LLMClient


class BedrockConverseClient(LLMClient):
    client: boto3.client = None

    def __init__(self):
        boto3.setup_default_session(profile_name=AWS_PROFILE)

        self.client = boto3.client(
            service_name="bedrock-runtime", region_name=AWS_REGION_FRANKFURT
        )

    def _encode_image(self, image_path: str) -> str:
        """Encode image file to base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def _get_media_type(self, image_path: str) -> str:
        """Get media type based on file extension"""
        extension = image_path.lower().split(".")[-1]
        media_types = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "webp": "image/webp",
        }
        return media_types.get(extension, "image/jpeg")

    def invoke_model(
        self,
        model_id: str,
        system_prompt: str,
        user_prompt: str,
        image_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        # Build user content with image first, then text
        user_content = []

        # Add image first if provided
        if image_path:
            image_base64 = self._encode_image(image_path)
            media_type = self._get_media_type(image_path)

            user_content.append(
                {
                    "image": {
                        "format": media_type.split("/")[-1],
                        "source": {"bytes": base64.b64decode(image_base64)},
                    }
                }
            )

        # Add text after image
        user_content.append({"text": user_prompt})

        # Prepare messages for Converse API
        messages = [
            {
                "role": "user",
                "content": user_content,
            }
        ]

        # System message configuration
        system_messages = []
        if system_prompt:
            system_messages = [{"text": system_prompt}]

        # Configure inference parameters
        inference_config = {
            "maxTokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "topP": TOP_P,
            "stopSequences": ["\n\nHuman:", "\n\nAssistant", "</function_calls>"],
        }

        # Additional model-specific configuration for Anthropic models
        additional_model_request_fields = {}
        if "anthropic" in model_id.lower():
            additional_model_request_fields = {"top_k": TOP_K}

        # Use Converse API
        response = self.client.converse(
            modelId=model_id,
            messages=messages,
            system=system_messages,
            inferenceConfig=inference_config,
            additionalModelRequestFields=additional_model_request_fields,
        )

        return {
            'content': [{'text': response['output']['message']['content'][0]['text']}]
        }
    
    def get_client_type(self) -> str:
        return "Bedrock Converse API"
