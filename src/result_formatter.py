class ResultFormatter:
    def format_single_result(self, attack_name: str, injection_detected: bool, response_text: str) -> str:
        status = '❌ Injection successful' if injection_detected else '✅ Injection failed'
        return f"""{attack_name}: {status}
        output: {response_text}
        """

    def format_single_result_with_iterations(
        self, attack_name: str, successful_iterations: int, blocked_iterations: int, success_rate: float, last_response: str
    ) -> str:
        total_iterations = successful_iterations + blocked_iterations
        status_icon = '❌' if success_rate > 0 else '✅'

        return f"""{attack_name}: {status_icon} {successful_iterations}/{total_iterations} injections successful ({success_rate:.1f}%)
        Successful: {successful_iterations}, Blocked: {blocked_iterations}
        Last output: {last_response}
        """

    def format_summary_stats(self, total_tests: int, blocked_injections: int, successful_injections: int) -> str:
        fail_rate = (successful_injections / total_tests) * 100 if total_tests > 0 else 0

        summary = f'Total: {total_tests}, Success: {blocked_injections}, Fail: {successful_injections}, Fail Rate: {fail_rate:.2f}%'

        print('\n' + '=' * 50)
        print(summary)
        print('=' * 50)

    def format_summary_stats_with_iterations(
        self, total_tests: int, total_iterations: int, blocked_injections: int, successful_injections: int
    ) -> str:
        attack_success_rate = (successful_injections / total_iterations) * 100 if total_iterations > 0 else 0
        defense_success_rate = 100 - attack_success_rate

        summary = f"""SECURITY TEST RESULTS
Total Attack Types: {total_tests} | Total Iterations: {total_iterations}
🛡️  Defense Success: {blocked_injections} ({defense_success_rate:.1f}%) - Attacks blocked
⚠️  Defense Failure: {successful_injections} ({attack_success_rate:.1f}%) - Attacks succeeded"""

        print('\n' + '=' * 70)
        print(summary)
        print('=' * 70)
