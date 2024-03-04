import sys
import toml

def update_version_in_toml(file_path, new_version):
    with open(file_path, 'r') as file:
        data = toml.load(file)

    data['tool']['poetry']['version'] = new_version

    with open(file_path, 'w') as file:
        toml.dump(data, file)

if __name__ == "__main__":
    file_path = sys.argv[1]
    new_version = sys.argv[2]
    update_version_in_toml(file_path, new_version)
