import os
import requests
import base64

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'your-username'
REPO_NAME = 'your-repo'

def get_repo_contents(owner, repo, path=''):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def save_file_content(file_url, local_path):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(file_url, headers=headers)
    response.raise_for_status()
    content = response.json().get('content', '')
    decoded_content = base64.b64decode(content).decode('utf-8')
    with open(local_path, 'w', encoding='utf-8') as f:
        f.write(decoded_content)

def fetch_and_save_all_files(owner, repo, base_path=''):
    contents = get_repo_contents(owner, repo, base_path)
    for item in contents:
        if item['type'] == 'file':
            file_path = item['path']
            local_path = os.path.join('files', file_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            save_file_content(item['url'], local_path)
            print(f'Saved {file_path}')
        elif item['type'] == 'dir':
            fetch_and_save_all_files(owner, repo, item['path'])

if __name__ == "__main__":
    os.makedirs('files', exist_ok=True)
    fetch_and_save_all_files(REPO_OWNER, REPO_NAME)
