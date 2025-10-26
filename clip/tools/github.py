from typing import Dict, List
import requests, os

token = os.getenv("GITHUB_TOKEN")
owner = os.getenv("OWNER")

def get_pull_request(
        repository: str,
        pull_request_number: str
) -> Dict[str, any]:
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repository}/pulls/{pull_request_number}",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code // 100 != 2: 
        return {
            "status": "error",
            "body": f"error when getting pull request: {response.text}"
        }
    return response.json()

def get_pull_request_files(
        repository: str,
        pull_request_number: str
) -> List[Dict[str, any]]:
    all_files = []
    page = 1

    while True:
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repository}/pulls/{pull_request_number}/files",
            headers={"Authorization": f"Bearer {token}"},
            params={"per_page": 100, "page": page}
        )

        if response.status_code // 100 != 2: 
            return {
                "status": "error",
                "body": f"Error when getting pull request files: {response.text}"
            }
        
        files = response.json()
        all_files.extend(files)

        if len(files) < 100:
            break

        page += 1

    return all_files