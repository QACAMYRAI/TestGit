import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')

BASE_URL = 'https://api.github.com'


def create_repository():
    url = f'{BASE_URL}/user/repos'
    payload = {
        "name": REPO_NAME,
        "private": False
    }
    response = requests.post(url, json=payload, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    return response


def check_repository_exists():
    url = f'{BASE_URL}/users/{GITHUB_USERNAME}/repos'
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    repos = response.json()
    return any(repo['name'] == REPO_NAME for repo in repos)


def delete_repository():
    url = f'{BASE_URL}/repos/{GITHUB_USERNAME}/{REPO_NAME}'
    response = requests.delete(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    return response.status_code


def test_full_check():
    # Создание репозитория
    create_response = create_repository()
    if create_response.status_code == 201:
        print(f'Repository "{REPO_NAME}" created successfully.')
    else:
        print(f'Failed to create repository: {create_response.json()}')
        return

    # Проверка существования репозитория
    if check_repository_exists():
        print(f'Repository "{REPO_NAME}" exists.')
    else:
        print(f'Repository "{REPO_NAME}" does not exist.')

    # Удаление репозитория
    delete_status = delete_repository()
    if delete_status == 204:
        print(f'Repository "{REPO_NAME}" deleted successfully.')
    else:
        print(f'Failed to delete repository: {delete_status}')


