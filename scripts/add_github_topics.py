#!/usr/bin/env python3
"""Script to add GitHub topics to the repository."""
from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library is required.")
    print("Install it with: pip install requests")
    sys.exit(1)

# Repository information
REPO_OWNER = "Jackngl"
REPO_NAME = "pioneer_avr_lx83"

# Topics to add
TOPICS = [
    "home-assistant",
    "homeassistant",
    "hacs",
    "custom-component",
    "integration",
    "pioneer",
    "avr",
    "amplifier",
    "home-automation",
    "iot",
]


def get_github_token() -> str | None:
    """Get GitHub token from environment or file."""
    # Try environment variable first
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return token

    # Try to read from .github_token file
    token_file = Path.home() / ".github_token"
    if token_file.exists():
        return token_file.read_text(encoding="utf-8").strip()

    # Try to read from local .github_token file
    local_token_file = Path(__file__).parent.parent / ".github_token"
    if local_token_file.exists():
        return local_token_file.read_text(encoding="utf-8").strip()

    return None


def get_current_topics(token: str) -> list[str]:
    """Get current topics from GitHub repository."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/topics"
    headers = {
        "Accept": "application/vnd.github.mercy-preview+json",
        "Authorization": f"token {token}",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("names", [])
    except requests.exceptions.RequestException as err:
        print(f"Error fetching current topics: {err}")
        return []


def set_topics(token: str, topics: list[str]) -> bool:
    """Set topics for GitHub repository."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/topics"
    headers = {
        "Accept": "application/vnd.github.mercy-preview+json",
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
    }
    data = {"names": topics}

    try:
        response = requests.put(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as err:
        print(f"Error setting topics: {err}")
        if hasattr(err.response, "text"):
            print(f"Response: {err.response.text}")
        return False


def main() -> None:
    """Main function."""
    print(f"Adding topics to {REPO_OWNER}/{REPO_NAME}...")
    print()

    # Get GitHub token
    token = get_github_token()
    if not token:
        print("Error: GitHub token not found!")
        print()
        print("Please provide a GitHub token in one of these ways:")
        print("1. Set GITHUB_TOKEN environment variable:")
        print("   export GITHUB_TOKEN=your_token_here")
        print("2. Create a file ~/.github_token with your token")
        print("3. Create a file .github_token in the project root")
        print()
        print("To create a token:")
        print("1. Go to https://github.com/settings/tokens")
        print("2. Click 'Generate new token (classic)'")
        print("3. Select scope: 'public_repo'")
        print("4. Copy the token and use it as described above")
        sys.exit(1)

    # Get current topics
    print("Fetching current topics...")
    current_topics = get_current_topics(token)
    print(f"Current topics: {', '.join(current_topics) if current_topics else 'None'}")
    print()

    # Merge topics (keep existing, add new ones)
    all_topics = list(set(current_topics + TOPICS))
    all_topics.sort()

    print(f"Topics to set ({len(all_topics)}):")
    for topic in all_topics:
        marker = "  [existing]" if topic in current_topics else "  [new]"
        print(f"  {topic}{marker}")
    print()

    # Confirm
    response = input("Do you want to update the topics? (yes/no): ").strip().lower()
    if response not in ["yes", "y"]:
        print("Cancelled.")
        sys.exit(0)

    # Set topics
    print("Setting topics...")
    if set_topics(token, all_topics):
        print("✅ Topics successfully updated!")
        print()
        print(f"Repository: https://github.com/{REPO_OWNER}/{REPO_NAME}")
        print("You can verify the topics on the repository page.")
    else:
        print("❌ Failed to update topics.")
        sys.exit(1)


if __name__ == "__main__":
    main()

