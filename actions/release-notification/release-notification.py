import os
import sys
import requests
import re
from github import Github
import json
from datetime import datetime, timedelta, timezone
import time
import subprocess
from packaging import version
import traceback

def is_valid_tag(tag_string):
    """
    Check if a given string is a valid tag with a prefix and semantic version.
    """
    tag_pattern = r'^(.+)-(\d+\.\d+\.\d+)$'
    match = re.match(tag_pattern, tag_string)
    if match:
        prefix, version = match.groups()
        # Ensure the prefix only contains letters, numbers, and hyphens
        if re.match(r'^[a-zA-Z0-9-]+$', prefix):
            return True
    return False

def parse_tag(tag_name):
    """
    Parse a tag name to extract the prefix and version number.
    """
    match = re.match(r'^(.+)-(\d+\.\d+\.\d+)$', tag_name)
    if match:
        prefix, version = match.groups()
        # Ensure the prefix only contains letters, numbers, and hyphens
        if re.match(r'^[a-zA-Z0-9-]+$', prefix):
            return prefix, version
    return None, None

def get_release_info():
    """
    Retrieves the GitHub tag from the environment variable.
    """
    repo = os.environ.get('GITHUB_REPOSITORY')
    current_tag = os.environ.get('GITHUB_REF').replace('refs/tags/', '')

    prefix, version = parse_tag(current_tag)
    if not prefix or not version:
        raise ValueError(f"Invalid version tag format: {current_tag}")

    return {
        "tag": current_tag,
        "prefix": prefix,
        "version": version,
        "repo": repo
    }

def get_previous_tag(repo, current_tag, access_token):
    g = Github(access_token)
    repo = g.get_repo(repo)

    cutoff_date = (datetime.utcnow() - timedelta(days=180)).replace(tzinfo=timezone.utc)

    valid_tags = []
    
    git_command = [
        'git',
        'log',
        '--tags',
        '--simplify-by-decoration',
        '--pretty=format:%ai %d'
    ]
    
    try:
        process = subprocess.run(git_command, capture_output=True, text=True, check=True)
        output = process.stdout
        
        for line in output.strip().split('\n'):
            match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [+-]\d{4}).*\(tag: (.+?)\)', line)
            if match:
                date_str, tag = match.groups()
                commit_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S %z')
                if commit_date >= cutoff_date and tag != current_tag['tag']:
                    prefix, version_str = parse_tag(tag)
                    if prefix == current_tag['prefix'] and version_str and is_valid_tag(tag):
                        valid_tags.append({'tag': tag, 'date': commit_date, 'version': version_str})

    except subprocess.CalledProcessError as e:
        print(f"Error executing git command: {e}")
        return None, None

    if not valid_tags:
        raise ValueError(f"No valid tags with prefix '{current_tag['prefix']}' found in the last 180 days")

    sorted_tags = sorted(valid_tags, key=lambda t: version.parse(t['version']), reverse=True)
    latest_tag = sorted_tags[0] if sorted_tags else None

    if latest_tag is None:
        raise ValueError(f"No valid previous tag with prefix '{current_tag['prefix']}' found")

    try:
        latest_release = repo.get_latest_release()
    except Exception as e:
        print(f"Warning: Unable to get latest release. Error: {e}")
        latest_release = None
    
    return latest_tag, latest_release

def compare_versions(previous_tag, current_version):
    prev_version = version.parse(previous_tag['version'])
    curr_version = version.parse(current_version)
    
    if curr_version.major > prev_version.major:
        return "major"
    elif curr_version.minor > prev_version.minor:
        return "minor"
    elif curr_version.micro > prev_version.micro:
        return "patch"
    else:
        return None

def send_slack_notification(webhook_url, message):
    print(message)
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook_url, json=message, headers=headers)

    if response.status_code == 200:
        print("Notification sent successfully to Slack!")
    else:
        print(f"Failed to send notification to Slack. Status code: {response.status_code}, Response: {response.text}")

def format_release_notes(body):
    if body is None:
        return "No release notes available."
    max_length = 2000
    if len(body) > max_length:
        body = body[:max_length] + "...\n(Release notes truncated due to length)"
    return body

if __name__ == "__main__":
    access_token = os.environ.get('GITHUB_TOKEN')
    current_tag = get_release_info()
    repo = current_tag["repo"]
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']

    print("Current Tag is: ", current_tag["tag"])
    print("Current Prefix is: ", current_tag["prefix"])
    print("Current Version is: ", current_tag["version"])

    try:
        previous_tag, latest_release = get_previous_tag(current_tag["repo"], current_tag, access_token)
        print("Last Tag with same prefix: ", previous_tag["tag"])
        print("Last Version with same prefix: ", previous_tag["version"])
        
        print(f"Debug: previous_tag = {previous_tag}")
        print(f"Debug: current_tag = {current_tag}")
        
        change_type = compare_versions(previous_tag, current_tag["version"])

        if change_type in ["major", "minor"]:
            formatted_body = format_release_notes(latest_release.body if latest_release else None)

            message = {
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"New Release on {repo}"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Current Tag:* `{current_tag['tag']}`"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Previous Tag:* `{previous_tag['tag']}`"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Change Type:* {change_type.capitalize()} version change"
                            }
                        ]
                    }
                ]
            }

            if latest_release:
                message["blocks"].append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Last Release on:* {latest_release.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                    }
                })

            message["blocks"].extend([
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Release Notes:*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"```{formatted_body}```"
                    }
                }
            ])

            if latest_release:
                message["blocks"].append({
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "View on GitHub"
                            },
                            "url": latest_release.html_url
                        }
                    ]
                })

            send_slack_notification(slack_webhook_url, message)
        else:
            print("No major or minor version changes")
        print()
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Traceback:")
        traceback.print_exc()