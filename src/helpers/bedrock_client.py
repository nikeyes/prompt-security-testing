import base64
import json
from typing import Optional

import boto3


class BedrockClient:
    client: boto3.client = None

    def __init__(self):
        boto3.setup_default_session(profile_name='ka-poc-ads-pre')

        aws_region_frankfurt = 'eu-central-1'

        self.client = boto3.client(service_name='bedrock-runtime', region_name=aws_region_frankfurt)

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
    ):
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
                'max_tokens': 2048,
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
                'temperature': 0.8,
                'top_k': 250,
                'top_p': 0.999,
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
