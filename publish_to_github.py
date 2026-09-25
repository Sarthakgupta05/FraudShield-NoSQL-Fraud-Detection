"""
Publish project to GitHub using GitHub Contents API & Git Data API.
Handles empty repo initialization and commits all workspace files.
"""

import os
import subprocess
import base64
import requests

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_NAME = "FraudShield-NoSQL-Fraud-Detection"
REPO_DESC = "FraudShield: Real-Time Multi-Model NoSQL Financial Fraud Detection System (MongoDB + Neo4j Property Graph Model)"
IS_PRIVATE = False

IGNORED_DIRS = {".git", "__pycache__", ".pytest_cache", "venv", "env", ".system_generated"}
IGNORED_FILES = {".DS_Store"}

def get_gh_token():
    res = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True)
    return res.stdout.strip()

def get_gh_username(token):
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    res = requests.get("https://api.github.com/user", headers=headers)
    res.raise_for_status()
    return res.json()["login"]

def ensure_repo(owner, token):
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    check_res = requests.get(f"https://api.github.com/repos/{owner}/{REPO_NAME}", headers=headers)
    if check_res.status_code == 200:
        return check_res.json()
    
    payload = {
        "name": REPO_NAME,
        "description": REPO_DESC,
        "private": IS_PRIVATE,
        "auto_init": False
    }
    create_res = requests.post("https://api.github.com/user/repos", headers=headers, json=payload)
    create_res.raise_for_status()
    return create_res.json()

def ensure_initial_commit(owner, token):
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    ref_res = requests.get(f"https://api.github.com/repos/{owner}/{REPO_NAME}/git/ref/heads/main", headers=headers)
    if ref_res.status_code == 200:
        return
    
    # Initialize with README.md via Contents API
    readme_path = os.path.join(WORKSPACE_DIR, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "rb") as f:
            content_b64 = base64.b64encode(f.read()).decode("utf-8")
    else:
        content_b64 = base64.b64encode(b"# FraudShield").decode("utf-8")

    put_res = requests.put(
        f"https://api.github.com/repos/{owner}/{REPO_NAME}/contents/README.md",
        headers=headers,
        json={
            "message": "Initial commit",
            "content": content_b64,
            "branch": "main"
        }
    )
    put_res.raise_for_status()
    print("Repository initialized with main branch.")

def collect_files():
    file_list = []
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".")]
        for file in files:
            if file in IGNORED_FILES or file.endswith(".pyc"):
                continue
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, WORKSPACE_DIR)
            file_list.append((rel_path, abs_path))
    return file_list

def upload_all_files(owner, token):
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    ensure_initial_commit(owner, token)
    
    files = collect_files()
    print(f"Total files to commit: {len(files)}")

    tree_entries = []
    for rel_path, abs_path in files:
        with open(abs_path, "rb") as f:
            content_bytes = f.read()
        
        b64_content = base64.b64encode(content_bytes).decode("utf-8")
        blob_res = requests.post(
            f"https://api.github.com/repos/{owner}/{REPO_NAME}/git/blobs",
            headers=headers,
            json={"content": b64_content, "encoding": "base64"}
        )
        blob_res.raise_for_status()
        blob_sha = blob_res.json()["sha"]
        
        tree_entries.append({
            "path": rel_path.replace("\\", "/"),
            "mode": "100644",
            "type": "blob",
            "sha": blob_sha
        })
        print(f"  ✓ Processed blob: {rel_path}")

    # Create Tree
    print("Creating git tree...")
    tree_res = requests.post(
        f"https://api.github.com/repos/{owner}/{REPO_NAME}/git/trees",
        headers=headers,
        json={"tree": tree_entries}
    )
    tree_res.raise_for_status()
    tree_sha = tree_res.json()["sha"]

    # Get parent commit on main
    ref_res = requests.get(f"https://api.github.com/repos/{owner}/{REPO_NAME}/git/ref/heads/main", headers=headers)
    ref_res.raise_for_status()
    parent_sha = ref_res.json()["object"]["sha"]

    # Create Commit
    commit_msg = "Complete FraudShield Multi-Model NoSQL Project & Assignment Artifacts"
    commit_res = requests.post(
        f"https://api.github.com/repos/{owner}/{REPO_NAME}/git/commits",
        headers=headers,
        json={
            "message": commit_msg,
            "tree": tree_sha,
            "parents": [parent_sha]
        }
    )
    commit_res.raise_for_status()
    commit_sha = commit_res.json()["sha"]
    print(f"Created commit: {commit_sha}")

    # Update Ref
    update_ref = requests.patch(
        f"https://api.github.com/repos/{owner}/{REPO_NAME}/git/refs/heads/main",
        headers=headers,
        json={"sha": commit_sha, "force": True}
    )
    update_ref.raise_for_status()

    repo_url = f"https://github.com/{owner}/{REPO_NAME}"
    print("\n" + "="*60)
    print("SUCCESS: Published project to GitHub!")
    print(f"Repository URL: {repo_url}")
    print("="*60)
    return repo_url

if __name__ == "__main__":
    token = get_gh_token()
    username = get_gh_username(token)
    print(f"Authenticated as GitHub user: {username}")
    ensure_repo(username, token)
    upload_all_files(username, token)
