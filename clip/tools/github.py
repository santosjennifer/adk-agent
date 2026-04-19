from typing import Dict, List, Optional
import requests, os

token = os.getenv("GITHUB_TOKEN")
default_owner = os.getenv("OWNER")

def resolve_owner(owner: Optional[str]) -> str:
    return owner or default_owner

def get_pull_request(
    repository: str,
    pull_request_number: str,
    owner: Optional[str] = None
) -> Dict[str, any]:
    final_owner = resolve_owner(owner)

    response = requests.get(
        f"https://api.github.com/repos/{final_owner}/{repository}/pulls/{pull_request_number}",
        headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code // 100 != 2:
        return {
            "status": "error",
            "body": f"Error when getting pull request: {response.text}"
        }

    return response.json()

def get_pull_request_files(
    repository: str,
    pull_request_number: str,
    owner: Optional[str] = None
) -> List[Dict[str, any]]:
    final_owner = resolve_owner(owner)

    all_files = []
    page = 1

    while True:
        response = requests.get(
            f"https://api.github.com/repos/{final_owner}/{repository}/pulls/{pull_request_number}/files",
            headers={
                "Authorization": f"Bearer {token}"
            },
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

def get_pull_request_diff(
    repository: str,
    pull_request_number: str,
    owner: Optional[str] = None
) -> str:
    final_owner = resolve_owner(owner)

    response = requests.get(
        f"https://api.github.com/repos/{final_owner}/{repository}/pulls/{pull_request_number}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3.diff"
        }
    )

    if response.status_code // 100 != 2:
        return {
            "status": "error",
            "body": f"Error when getting pull request diff: {response.text}"
    }

    return response.text