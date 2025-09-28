from attack_loader import AttackLoader
from helpers.llm_client_factory import create_llm_client
from prompt_injection_tester import PromptInjectionTester
from prompt_to_test_loader import PromptToTestLoader


def main():
    prompt_to_test_loader = PromptToTestLoader()
    prompt_to_test = prompt_to_test_loader.load_prompt_to_test()

    bedrock_client = create_llm_client('converse')
    attack_loader = AttackLoader(attacks_dir=prompt_to_test['attacks_dir'])
    tester = PromptInjectionTester(bedrock_client, prompt_to_test['iterations'])

    attacks = attack_loader.load_yaml_attacks()
    attack_loader.display_attack_examples(attacks)

    tester.run_prompt_injection_tests(
        system_prompt=prompt_to_test['system_prompt'],
        pre_user_message=prompt_to_test['pre_user_message'],
        post_user_message=prompt_to_test['post_user_message'],
        attacks_list=attacks,
        model_id=prompt_to_test['model_id'],
    )


if __name__ == '__main__':
    main()
