import unittest
from pathlib import Path

from src.attack_loader import AttackLoader


class TestAttackLoader(unittest.TestCase):
    def setUp(self):
        self.test_attacks_dir = Path(__file__).parent / 'test_attacks'
        self.loader = AttackLoader(str(self.test_attacks_dir))

    def test_attack_loader_yaml_parsing(self):
        yaml_file = self.test_attacks_dir / 'valid_attack.yaml'

        loaded_attack = self.loader.load_attack_from_file(yaml_file)

        self.assertIsNotNone(loaded_attack)
        self.assertEqual(loaded_attack['name'], 'Test Attack Valid')
        self.assertEqual(loaded_attack['prompt'], 'Test prompt content for validation')
        self.assertEqual(loaded_attack['payload'], 'Expected test response')
        self.assertEqual(loaded_attack['type'], 'test injection')
        self.assertEqual(loaded_attack['source'], 'internal test')
        self.assertEqual(loaded_attack['licence_type'], 'MIT')
        self.assertEqual(loaded_attack['language'], 'en')

    def test_load_yaml_attacks_multiple_files(self):
        loaded_attacks = self.loader.load_yaml_attacks()

        self.assertGreaterEqual(len(loaded_attacks), 2)

        valid_attack = next((a for a in loaded_attacks if a['name'] == 'Test Attack Valid'), None)
        unicode_attack = next(
            (a for a in loaded_attacks if a['name'] == 'Test Attack with émojis 🚀'),
            None,
        )

        self.assertIsNotNone(valid_attack)
        self.assertIsNotNone(unicode_attack)

        self.assertEqual(valid_attack['type'], 'test injection')
        self.assertEqual(unicode_attack['type'], 'unicode test')

    def test_yaml_parsing_with_unicode(self):
        yaml_file = self.test_attacks_dir / 'unicode_attack.yaml'

        loaded_attack = self.loader.load_attack_from_file(yaml_file)

        self.assertIsNotNone(loaded_attack)
        self.assertEqual(loaded_attack['name'], 'Test Attack with émojis 🚀')
        self.assertIn('spëcial', loaded_attack['prompt'])
        self.assertIn('中文', loaded_attack['prompt'])

    def test_invalid_attack_structure_rejection_empty_attack(self):
        result = self.loader.is_valid_attack_structure({})
        self.assertFalse(result)

    def test_invalid_attack_structure_rejection_missing_name(self):
        attack = {
            'prompt': 'Test prompt',
            'payload': 'Test payload',
            'type': 'test injection',
            'source': 'internal test',
            'licence_type': 'MIT',
            'licence_url': 'https://opensource.org/licenses/MIT',
            'language': 'en',
        }
        result = self.loader.is_valid_attack_structure(attack)
        self.assertFalse(result)

    def test_invalid_attack_structure_rejection_missing_prompt(self):
        attack = {
            'name': 'Test Attack',
            'payload': 'Test payload',
            'type': 'test injection',
            'source': 'internal test',
            'licence_type': 'MIT',
            'licence_url': 'https://opensource.org/licenses/MIT',
            'language': 'en',
        }
        result = self.loader.is_valid_attack_structure(attack)
        self.assertFalse(result)

    def test_invalid_attack_structure_rejection_missing_payload(self):
        attack = {
            'name': 'Test Attack',
            'prompt': 'Test prompt',
            'type': 'test injection',
            'source': 'internal test',
            'licence_type': 'MIT',
            'licence_url': 'https://opensource.org/licenses/MIT',
            'language': 'en',
        }
        result = self.loader.is_valid_attack_structure(attack)
        self.assertFalse(result)

    def test_invalid_attack_structure_rejection_empty_required_fields(self):
        attack = {
            'name': '',
            'prompt': 'Test prompt',
            'payload': 'Test payload',
            'type': 'test injection',
            'source': 'internal test',
            'licence_type': 'MIT',
            'licence_url': 'https://opensource.org/licenses/MIT',
            'language': 'en',
        }
        result = self.loader.is_valid_attack_structure(attack)
        self.assertFalse(result)

    def test_valid_attack_structure_acceptance_complete(self):
        attack = {
            'name': 'Valid Test Attack',
            'prompt': 'Test prompt content',
            'payload': 'Expected response',
            'type': 'test injection',
            'source': 'internal test',
            'licence_type': 'MIT',
            'licence_url': 'https://opensource.org/licenses/MIT',
            'language': 'en',
        }
        result = self.loader.is_valid_attack_structure(attack)
        self.assertTrue(result)

    def test_valid_attack_structure_acceptance_with_image_not_exist(self):
        attack = {
            'name': 'Valid Image Attack',
            'prompt': 'Test prompt with image',
            'payload': 'Expected response',
            'image_path': 'test_image.jpeg',
            'type': 'test injection',
            'source': 'internal test',
            'licence_type': 'MIT',
            'licence_url': 'https://opensource.org/licenses/MIT',
            'language': 'en',
        }
        result = self.loader.is_valid_attack_structure(attack)
        self.assertFalse(result)

    def test_valid_attack_structure_acceptance_with_image_that_exists(self):
        attack = {
            'name': 'Valid Image Attack',
            'prompt': 'Test prompt with image',
            'payload': 'Expected response',
            'image_path': 'image_black.jpeg',
            'type': 'test injection',
            'source': 'internal test',
            'licence_type': 'MIT',
            'licence_url': 'https://opensource.org/licenses/MIT',
            'language': 'en',
        }
        result = self.loader.is_valid_attack_structure(attack)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
