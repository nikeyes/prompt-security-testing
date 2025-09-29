from pathlib import Path

import yaml


class AttackLoader:
    def __init__(self, attacks_dir):
        self.attacks_dir = attacks_dir

    def is_valid_attack_structure(self, attack_data):
        if not (attack_data and 'name' in attack_data and 'prompt' in attack_data and 'payload' in attack_data):
            return False

        # Check that required fields are not empty
        if not (attack_data['name'].strip() and attack_data['prompt'].strip() and attack_data['payload'].strip()):
            return False

        if 'image_path' in attack_data and attack_data['image_path']:
            image_path = Path(self.attacks_dir) / 'shared_assets' / attack_data['image_path']
            if not image_path.exists():
                image_path = Path(self.attacks_dir) / attack_data['image_path']

            if image_path.exists():
                attack_data['image_path'] = str(image_path)
            else:
                print(f'Error: Image file {attack_data["image_path"]} not found')
                return False
        else:
            attack_data['image_path'] = None

        return True

    def load_attack_from_file(self, yaml_file):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                attack_data = yaml.safe_load(f)
                if self.is_valid_attack_structure(attack_data):
                    # Add filename and file path information
                    attack_data['filename'] = yaml_file.name
                    attack_data['file_path'] = str(yaml_file.resolve())
                    # Add relative path from attacks directory
                    attacks_path = Path(self.attacks_dir).resolve()
                    attack_data['relative_path'] = str(yaml_file.resolve().relative_to(attacks_path))
                    return attack_data
                print(f'Invalid structure in {yaml_file.name}')
                return None
        except Exception as e:
            print(f'Failed to load {yaml_file.name}: {e}')
            return None

    def find_yaml_files(self):
        attacks_path = Path(self.attacks_dir)
        # Use recursive glob to find YAML files in all subdirectories
        return list(attacks_path.glob('**/*.yaml'))

    def load_yaml_attacks(self):
        yaml_files = self.find_yaml_files()
        print(f'Found {len(yaml_files)} YAML files')

        attacks = []
        for yaml_file in yaml_files:
            attack = self.load_attack_from_file(yaml_file)
            if attack:
                attacks.append(attack)

        print(f'Loaded {len(attacks)} valid attacks')
        return attacks

    def display_attack_examples(self, attacks, max_examples=3):
        print('\nLoaded attack examples:')
        for i, attack in enumerate(attacks[:max_examples]):
            attack_type = attack.get('type', 'N/A')
            payload_preview = attack['payload'][:50] + '...' if len(attack['payload']) > 50 else attack['payload']
            has_image = ' + 🌠 Image' if attack.get('image_path') else ''
            filename = attack.get('filename', 'N/A')
            print(f'{i + 1}. {attack["name"]} ({attack_type}){has_image}')
            print(f'   File: {filename}')
            print(f'   Payload: {payload_preview}')
            if attack.get('image_path'):
                print(f'   Image: {attack.get("image_path", "N/A")}')
            print()
