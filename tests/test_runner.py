import unittest
from unittest.mock import Mock

from src.prompt_injection_detector import PromptInjectionDetector
from src.result_formatter import ResultFormatter
from src.runner import Runner


class TestRunner(unittest.TestCase):
    def setUp(self):
        self.mock_bedrock_client = Mock()
        self.detector = PromptInjectionDetector(self.mock_bedrock_client)
        self.formatter = ResultFormatter()
        self.runner = Runner(self.detector, self.formatter, iterations=3)

    def test_run_injection_tests_basic_execution(self):
        # Mock Bedrock response for detected injection
        self.mock_bedrock_client.invoke_model.return_value = {'content': [{'text': 'Access Denied'}]}

        # Test data
        attacks_list_one_element = [
            {
                'name': 'Test Attack',
                'prompt': 'Test prompt',
                'payload': 'Access Denied',
            },
        ]

        result = self.runner.run_injection_tests(
            system_prompt='You are a helpful assistant',
            pre_user_message='Pre message',
            post_user_message='Post message',
            attacks_list=attacks_list_one_element,
            model_id='test-model',
        )

        self.assertEqual(result['total_tests'], 1)
        self.assertEqual(result['total_iterations'], 3)
        self.assertEqual(result['blocked_injections'], 0)
        self.assertEqual(result['successful_injections'], 3)

        test_result = result['results'][0]

        self.assertEqual(test_result['name'], 'Test Attack')
        self.assertEqual(test_result['iterations'], 3)
        self.assertEqual(test_result['successful_iterations'], 3)
        self.assertEqual(test_result['blocked_iterations'], 0)
        self.assertEqual(test_result['success_rate'], 100.0)
        self.assertEqual(len(test_result['iteration_results']), 3)

        self.assertEqual(self.mock_bedrock_client.invoke_model.call_count, 3)

    def test_run_injection_tests_complex_execution(self):
        # Mock Bedrock response for detected injection
        self.mock_bedrock_client.invoke_model.return_value = {'content': [{'text': 'Access Denied'}]}

        # Test data
        # Test data
        attacks_list_two_element = [
            {
                'name': 'Test Attack 1',
                'prompt': 'Test prompt 1',
                'payload': 'Access Denied',
            },
            {
                'name': 'Test Attack 2',
                'prompt': 'Test prompt 2',
                'payload': 'I cannot complete this action.',
            },
        ]

        result = self.runner.run_injection_tests(
            system_prompt='You are a helpful assistant',
            pre_user_message='Pre message',
            post_user_message='Post message',
            attacks_list=attacks_list_two_element,
            model_id='test-model',
        )

        self.assertEqual(result['total_tests'], 2)
        self.assertEqual(result['total_iterations'], 6)
        self.assertEqual(result['blocked_injections'], 3)
        self.assertEqual(result['successful_injections'], 3)

        test_result1 = result['results'][0]

        self.assertEqual(test_result1['name'], 'Test Attack 1')
        self.assertEqual(test_result1['iterations'], 3)
        self.assertEqual(test_result1['successful_iterations'], 3)
        self.assertEqual(test_result1['blocked_iterations'], 0)
        self.assertEqual(test_result1['success_rate'], 100.0)
        self.assertEqual(len(test_result1['iteration_results']), 3)

        test_result2 = result['results'][1]

        self.assertEqual(test_result2['name'], 'Test Attack 2')
        self.assertEqual(test_result2['iterations'], 3)
        self.assertEqual(test_result2['successful_iterations'], 0)
        self.assertEqual(test_result2['blocked_iterations'], 3)
        self.assertEqual(test_result2['success_rate'], 0.0)
        self.assertEqual(len(test_result2['iteration_results']), 3)

        # Verify Bedrock was called correctly (3 iterations)
        self.assertEqual(self.mock_bedrock_client.invoke_model.call_count, 6)


if __name__ == '__main__':
    unittest.main()
