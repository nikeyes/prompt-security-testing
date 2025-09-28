from pathlib import Path
from typing import Any, Dict

import yaml


class PromptToTestLoader:
    def __init__(self, use_case: str = 'default', config_path: str = None):
        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = Path(f'use_cases/{use_case}/prompt_to_test.yaml')

    def load_prompt_to_test(self) -> Dict[str, Any]:
        """Load prompt testing configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f'Configuration file not found: {self.config_path}')

        with open(self.config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)

        return config
