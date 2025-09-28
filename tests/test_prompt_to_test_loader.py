import unittest
import tempfile
import yaml
from pathlib import Path

from src.prompt_to_test_loader import PromptToTestLoader


class TestPromptToTestLoader(unittest.TestCase):
    def setUp(self):
        self.test_config_data = {
            'model_id': 'test-model-id',
            'attacks_dir': 'test/attacks',
            'iterations': 5,
            'system_prompt': 'Test system prompt',
            'pre_user_message': '<test>',
            'post_user_message': 'Test post message</test>'
        }

    def test_load_valid_config(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.test_config_data, f)
            config_path = f.name

        try:
            loader = PromptToTestLoader(config_path)
            config = loader.load_prompt_to_test()

            self.assertEqual(config['model_id'], 'test-model-id')
            self.assertEqual(config['attacks_dir'], 'test/attacks')
            self.assertEqual(config['iterations'], 5)
            self.assertEqual(config['system_prompt'], 'Test system prompt')
            self.assertEqual(config['pre_user_message'], '<test>')
            self.assertEqual(config['post_user_message'], 'Test post message</test>')
        finally:
            Path(config_path).unlink()

    def test_file_not_found_raises_exception(self):
        loader = PromptToTestLoader('nonexistent_file.yaml')

        with self.assertRaises(FileNotFoundError) as context:
            loader.load_prompt_to_test()

        self.assertIn('Configuration file not found', str(context.exception))

    def test_default_config_path(self):
        loader = PromptToTestLoader()
        self.assertEqual(str(loader.config_path), 'use_cases/default/prompt_to_test.yaml')

    def test_custom_config_path(self):
        custom_path = 'custom/path/config.yaml'
        loader = PromptToTestLoader(custom_path)
        self.assertEqual(str(loader.config_path), custom_path)


if __name__ == '__main__':
    unittest.main()