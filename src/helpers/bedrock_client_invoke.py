import base64
import json
from typing import Any, Dict, Optional

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


class BedrockInvokeClient(LLMClient):
    client: boto3.client = None

    def __init__(self):
        boto3.setup_default_session(profile_name=AWS_PROFILE)
        self.client = boto3.client(service_name='bedrock-runtime', region_name=AWS_REGION_FRANKFURT)

    def _encode_image(self, image_path: str) -> str:
        """Encode image file to base64 string"""
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _get_media_type(self, image_path: str) -> str:
        """Get media type based on file extension"""
        extension = image_path.lower().split('.')[-1]
        media_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp',
        }
        return media_types.get(extension, 'image/jpeg')

    def invoke_model(
        self,
        model_id: str,
        system_prompt: str,
        user_prompt: str,
        image_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        # Validate that the model is supported by this client
        if 'anthropic' not in model_id.lower():
            raise ValueError(
                f'BedrockInvokeClient only supports Anthropic models. '
                f"Model '{model_id}' is not supported. "
                f'Use BedrockConverseClient for other model families.'
            )

        # Build user content with image first, then text
        user_content = []

        # Add image first if provided
        if image_path:
            image_base64 = self._encode_image(image_path)
            media_type = self._get_media_type(image_path)

            user_content.append(
                {
                    'type': 'image',
                    'source': {
                        'type': 'base64',
                        'media_type': media_type,
                        'data': image_base64,
                    },
                }
            )

        # Add text after image
        user_content.append({'type': 'text', 'text': user_prompt})

        body = json.dumps(
            {
                'system': system_prompt,
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': MAX_TOKENS,
                'messages': [
                    {
                        'role': 'user',
                        'content': user_content,
                    },
                    {
                        'role': 'assistant',
                        'content': '',
                    },
                ],
                'temperature': TEMPERATURE,
                'top_k': TOP_K,
                'top_p': TOP_P,
                'stop_sequences': ['\n\nHuman:', '\n\nAssistant', '</function_calls>'],
            }
        )

        accept = 'application/json'
        content_type = 'application/json'

        response = self.client.invoke_model(
            modelId=model_id,
            body=body,
            accept=accept,
            contentType=content_type,
        )

        completion = json.loads(response.get('body').read())
        return completion

    def get_client_type(self) -> str:
        return 'Bedrock Invoke API'
