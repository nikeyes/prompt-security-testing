from typing import Any, Dict, List

from helpers.llm_client import LLMClient
from prompt_injection_detector import PromptInjectionDetector
from result_formatter import ResultFormatter
from runner import Runner


class PromptInjectionTester:
    def __init__(self, bedrock_client: LLMClient, iterations: int = 3) -> None:
        self.bedrock_client = bedrock_client
        self.detector = PromptInjectionDetector(bedrock_client)
        self.formatter = ResultFormatter()
        self.runner = Runner(self.detector, self.formatter, iterations)

    def run_prompt_injection_tests(
        self,
        system_prompt: str,
        pre_user_message: str,
        post_user_message: str,
        attacks_list: List[Dict[str, Any]],
        model_id: str,
    ) -> Dict[str, Any]:
        stats = self.runner.run_injection_tests(system_prompt, pre_user_message, post_user_message, attacks_list, model_id)

        client_type = self.bedrock_client.get_client_type()

        self.formatter.format_summary_stats_with_iterations(
            stats['total_tests'],
            stats['total_iterations'],
            stats['blocked_injections'],
            stats['successful_injections'],
            client_type,
            model_id,
        )
