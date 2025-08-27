from typing import Any, Dict, List


class Runner:
    def __init__(self, detector: Any, formatter: Any, iterations: int = 3) -> None:
        self.detector = detector
        self.formatter = formatter
        self.iterations = iterations

    def run_injection_tests(
        self,
        system_prompt: str,
        pre_user_message: str,
        post_user_message: str,
        attacks_list: List[Dict[str, Any]],
        model_id: str,
    ) -> Dict[str, Any]:
        results = []
        blocked_injections = 0
        successful_injections = 0
        total_tests = len(attacks_list)
        total_iterations = total_tests * self.iterations

        for i, attack in enumerate(attacks_list, 1):
            attack_name = attack.get('name', 'Unknown Attack')
            attack_message = attack['prompt']
            attack_payload = attack['payload']
            attack_image_path = attack.get('image_path')

            icon = '🖼️ ' if attack_image_path else ''
            print(f'Test {i}/{total_tests}: {attack_name} - {icon}Running {self.iterations} iterations...')

            defended_message = f"""
                {pre_user_message}
                {attack_message}
                {post_user_message}
            """

            iteration_results = []
            successful_iterations = 0

            for iteration in range(self.iterations):
                detection_result = self.detector.detect_injection(
                    system_prompt,
                    defended_message,
                    attack_payload,
                    model_id,
                    attack_image_path,
                )

                iteration_results.append(
                    {
                        'iteration': iteration + 1,
                        'injection_detected': detection_result['injection_detected'],
                        'response_text': detection_result['response_text'],
                    }
                )

                if detection_result['injection_detected']:
                    successful_iterations += 1

            blocked_iterations = self.iterations - successful_iterations
            success_rate = (successful_iterations / self.iterations) * 100

            test_result = {
                'name': attack_name,
                'iterations': self.iterations,
                'successful_iterations': successful_iterations,
                'blocked_iterations': blocked_iterations,
                'success_rate': success_rate,
                'iteration_results': iteration_results,
            }

            results.append(test_result)

            successful_injections += successful_iterations
            blocked_injections += blocked_iterations

            output = self.formatter.format_single_result_with_iterations(
                attack_name, successful_iterations, blocked_iterations, success_rate, iteration_results[-1]['response_text']
            )
            print(output)

        return {
            'total_tests': total_tests,
            'total_iterations': total_iterations,
            'blocked_injections': blocked_injections,
            'successful_injections': successful_injections,
            'results': results,
        }
