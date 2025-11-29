"""
Agent Beta - Weekly Notification
Simple rule: Every Monday at 9 AM, count modules and create summary.
"""

import requests
from datetime import datetime
import os
from notion_config import NOTION_TOKEN

# Notion Configuration
NOTION_TOKEN = NOTION_TOKEN
MODULE_LIBRARY_DB = "eac1ce58-6169-4dc3-a821-29858ae59e76"
DEV_TASKS_DB = "662cbb0c-1cca-4c12-9991-c566f220eb0c"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS_LOG = os.path.join(BASE_DIR, "logs", "status_updates.log")

def weekly_notification():
    """Create weekly module status summary notification."""
    
    print("🤖 Agent Beta - Weekly Notification")
    print("=" * 50)
    
    # 1. Get all modules
    print("\n🔍 Querying all modules...")
    
    try:
        response = requests.post(
            f"https://api.notion.com/v1/databases/{MODULE_LIBRARY_DB}/query",
            headers=headers,
            json={}
        )
        response.raise_for_status()
        
        modules = response.json().get('results', [])
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error querying modules: {str(e)}")
        return
    
    print(f"📋 Found {len(modules)} total module(s)")
    
    # 2. Count by status
    counts = {"Draft": 0, "Published": 0, "Deployed": 0, "Archived": 0, "Unknown": 0}
    
    for module in modules:
        try:
            if 'properties' in module and 'Status' in module['properties']:
                status_prop = module['properties']['Status']
                if status_prop.get('select') and status_prop['select'].get('name'):
                    status = status_prop['select']['name']
                    if status in counts:
                        counts[status] += 1
                    else:
                        counts['Unknown'] += 1
                else:
                    counts['Unknown'] += 1
            else:
                counts['Unknown'] += 1
        except (KeyError, TypeError):
            counts['Unknown'] += 1
    
    print(f"\n📊 Status Summary:")
    for status, count in counts.items():
        if count > 0:
            print(f"   {status}: {count}")
    
    # 3. Create notification page
    today = datetime.now().strftime("%Y-%m-%d")
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json={
                "parent": {"database_id": DEV_TASKS_DB},
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": f"📊 Weekly Module Status - {today}"
                                }
                            }
                        ]
                    },
                    "Status": {"select": {"name": "Not Started"}},
                    "Priority": {"select": {"name": "P2 Medium"}}
                },
                "children": [
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"text": {"content": "Module Status Summary"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": f"📝 Draft: {counts['Draft']}"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": f"✅ Published: {counts['Published']}"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": f"🚀 Deployed: {counts['Deployed']}"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": f"📦 Archived: {counts['Archived']}"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": f"📊 Total: {len(modules)}"}}]
                        }
                    }
                ]
            }
        )
        response.raise_for_status()
        
        print(f"\n✅ Created weekly status notification in Development Tasks")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating notification: {str(e)}")
        return
    
    # 4. Log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(STATUS_LOG, 'a') as f:
        f.write(f"{timestamp}: Created weekly notification - {len(modules)} modules total\n")
    
    print(f"\n{'=' * 50}")
    print(f"📝 Log written to: {STATUS_LOG}")

if __name__ == "__main__":
    weekly_notification()
