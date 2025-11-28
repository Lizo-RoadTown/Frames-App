# Notion API Integration Guide

**Date:** 2025-11-28
**Notion API Version:** 2022-06-28
**Purpose:** Guide for interacting with Notion databases and pages

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [API Basics](#api-basics)
4. [Database Operations](#database-operations)
5. [Page Operations](#page-operations)
6. [Block Operations](#block-operations)
7. [Sync Workflow](#sync-workflow)
8. [Rate Limiting](#rate-limiting)
9. [Error Handling](#error-handling)
10. [Examples](#examples)

---

## Overview

### What We Use Notion For

FRAMES integrates with Notion for:
- **Content Authoring:** Team leads create content in Notion
- **Dashboard Presentation:** CADENCE Hub shows data from Postgres
- **Module Library:** Catalog of 68 training modules
- **Team Coordination:** Tasks, meetings, documents tracking

### Integration Architecture

```
┌─────────────────┐
│  Notion         │
│  Workspace      │
│                 │
│  • CADENCE Hub  │
│  • 5 Databases  │
└────────┬────────┘
         │
         ↓
   Notion API
   (REST, v2022-06-28)
         ↓
┌────────┴────────┐
│  Agent Beta     │
│  Sync Scripts   │
└────────┬────────┘
         │
         ↓
┌────────┴────────┐
│  PostgreSQL     │
│  (Neon)         │
│  Canonical Data │
└─────────────────┘
```

**Data Flow:**
- **Write:** Postgres → Notion (sync script)
- **Read:** Notion → Extract → Postgres (import script)

---

## Authentication

### Getting Notion API Token

1. Go to https://www.notion.so/my-integrations
2. Click "New integration"
3. Name: "FRAMES Integration"
4. Select workspace
5. Copy "Internal Integration Token"

### Configuration

**Environment Variable (.env):**
```bash
NOTION_TOKEN=ntn_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Python Usage:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv('NOTION_TOKEN')

HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}
```

### Sharing Databases with Integration

**Important:** Integration must have access to databases/pages

1. Open database in Notion
2. Click "..." menu → "Add connections"
3. Select "FRAMES Integration"
4. Grant "Read" and "Update" permissions

---

## API Basics

### Base URL

```
https://api.notion.com/v1
```

### Common Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/databases/{id}` | GET | Get database schema |
| `/databases/{id}/query` | POST | Query database records |
| `/pages` | POST | Create new page/record |
| `/pages/{id}` | GET | Get page details |
| `/pages/{id}` | PATCH | Update page properties |
| `/blocks/{id}` | GET | Get block details |
| `/blocks/{id}/children` | GET | Get child blocks |
| `/blocks/{id}/children` | PATCH | Append blocks |

### Request Format

**Headers:**
```http
Authorization: Bearer ntn_xxxxxxxxxxxxx
Content-Type: application/json
Notion-Version: 2022-06-28
```

**Example Request:**
```python
import requests

response = requests.get(
    f'https://api.notion.com/v1/databases/{database_id}',
    headers=HEADERS
)
```

---

## Database Operations

### Get Database Schema

**Purpose:** Retrieve database properties and structure

```python
def get_database_schema(database_id):
    url = f'https://api.notion.com/v1/databases/{database_id}'
    response = requests.get(url, headers=HEADERS)
    return response.json()

# Usage
schema = get_database_schema('eac1ce58-6169-4dc3-a821-29858ae59e76')
properties = schema['properties']
print(f"Database has {len(properties)} properties")
```

**Response:**
```json
{
  "object": "database",
  "id": "eac1ce58-6169-4dc3-a821-29858ae59e76",
  "title": [{"text": {"content": "📚 Module Library"}}],
  "properties": {
    "Name": {"title": {}},
    "Status": {"select": {"options": [...]}},
    "Category": {"select": {"options": [...]}},
    "Difficulty": {"select": {"options": [...]}}
  }
}
```

---

### Query Database

**Purpose:** Retrieve all records or filtered subset

**Basic Query (all records):**
```python
def query_database(database_id):
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    response = requests.post(url, headers=HEADERS, json={})
    return response.json()['results']

# Usage
modules = query_database('eac1ce58-6169-4dc3-a821-29858ae59e76')
print(f"Found {len(modules)} modules")
```

**Filtered Query:**
```python
def query_database_filtered(database_id, filters):
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    payload = {"filter": filters}
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()['results']

# Get published modules only
filter_published = {
    "property": "Status",
    "select": {"equals": "Published"}
}
published_modules = query_database_filtered(db_id, filter_published)
```

**Pagination:**
```python
def query_database_all(database_id):
    """Get all records with pagination"""
    all_results = []
    has_more = True
    start_cursor = None

    while has_more:
        payload = {}
        if start_cursor:
            payload['start_cursor'] = start_cursor

        url = f'https://api.notion.com/v1/databases/{database_id}/query'
        response = requests.post(url, headers=HEADERS, json=payload)
        data = response.json()

        all_results.extend(data['results'])
        has_more = data['has_more']
        start_cursor = data.get('next_cursor')

    return all_results
```

---

### Create Database

**Purpose:** Programmatically create new database

```python
def create_database(parent_page_id, title, properties):
    url = 'https://api.notion.com/v1/databases'
    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"text": {"content": title}}],
        "properties": properties
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

# Example: Create Team Members DB
properties = {
    "Name": {"title": {}},
    "Role": {
        "select": {
            "options": [
                {"name": "Team Lead", "color": "red"},
                {"name": "Engineer", "color": "blue"}
            ]
        }
    },
    "Email": {"email": {}},
    "Subsystem": {
        "select": {
            "options": [
                {"name": "Avionics", "color": "blue"},
                {"name": "Power", "color": "yellow"}
            ]
        }
    }
}

db = create_database(
    parent_page_id='2b76b8ea-578a-8040-b328-c8527dedea93',
    title='Team Members',
    properties=properties
)
print(f"Created database: {db['id']}")
```

---

## Page Operations

### Create Page (Database Record)

**Purpose:** Add new record to database

```python
def create_page(database_id, properties):
    url = 'https://api.notion.com/v1/pages'
    payload = {
        "parent": {"database_id": database_id},
        "properties": properties
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

# Example: Create team member
properties = {
    "Name": {
        "title": [{"text": {"content": "Alice Johnson"}}]
    },
    "Role": {
        "select": {"name": "Engineer"}
    },
    "Email": {
        "email": "alice@example.com"
    },
    "Subsystem": {
        "select": {"name": "Avionics"}
    }
}

page = create_page('2b96b8ea-578a-8165-905e-d8d01c403cc2', properties)
print(f"Created page: {page['id']}")
```

---

### Update Page

**Purpose:** Modify existing page properties

```python
def update_page(page_id, properties):
    url = f'https://api.notion.com/v1/pages/{page_id}'
    payload = {"properties": properties}
    response = requests.patch(url, headers=HEADERS, json=payload)
    return response.json()

# Example: Update person's role
updated = update_page(
    page_id='2b96b8ea-578a-8101-80f6-d78aea760980',
    properties={
        "Role": {"select": {"name": "Team Lead"}},
        "Status": {"select": {"name": "Active"}}
    }
)
```

---

### Get Page

**Purpose:** Retrieve page details

```python
def get_page(page_id):
    url = f'https://api.notion.com/v1/pages/{page_id}'
    response = requests.get(url, headers=HEADERS)
    return response.json()

page = get_page('2b96b8ea-578a-8101-80f6-d78aea760980')
title = page['properties']['Name']['title'][0]['text']['content']
print(f"Page title: {title}")
```

---

## Block Operations

### Get Block Children

**Purpose:** Retrieve content blocks from a page

```python
def get_block_children(block_id):
    url = f'https://api.notion.com/v1/blocks/{block_id}/children'
    response = requests.get(url, headers=HEADERS)
    return response.json()['results']

# Get all blocks from a page
blocks = get_block_children('2b86b8ea-578a-80cb-8f25-f080444ec266')
for block in blocks:
    print(f"{block['type']}")
```

---

### Append Blocks

**Purpose:** Add content blocks to a page

⚠️ **WARNING:** Per CADENCE spec, NEVER append blocks to dashboards!

```python
def append_blocks(page_id, blocks):
    """Use ONLY for non-dashboard pages"""
    url = f'https://api.notion.com/v1/blocks/{page_id}/children'
    payload = {"children": blocks}
    response = requests.patch(url, headers=HEADERS, json=payload)
    return response.json()

# Example: Add heading and paragraph (only to module pages, NOT dashboards)
blocks = [
    {
        "type": "heading_1",
        "heading_1": {
            "rich_text": [{"text": {"content": "Module Overview"}}]
        }
    },
    {
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"text": {"content": "This module covers..."}}]
        }
    }
]

# ONLY for module pages, NEVER dashboards
append_blocks(module_page_id, blocks)
```

---

## Sync Workflow

### Postgres → Notion Sync (7 Steps)

Per `cadence_spec_full/pipelines/pg_to_notion_workflow.md`:

**Step 1: Schema Discovery**
```python
def discover_schema():
    """Identify canonical tables"""
    tables = ['people', 'projects', 'tasks', 'meetings', 'documents']
    return tables
```

**Step 2: Data Extraction**
```python
def extract_data(table_name):
    """Query Postgres for all records"""
    from shared.database.cadence_models import get_model
    model = get_model(table_name)
    records = model.query.all()
    return [r.to_dict() for r in records]
```

**Step 3: Notion DB Resolution**
```python
def resolve_notion_dbs():
    """Load database IDs from config"""
    with open('notion_database_ids.json') as f:
        return json.load(f)

# Example: notion_database_ids.json
{
  "people": "2b96b8ea-578a-8165-905e-d8d01c403cc2",
  "projects": "...",
  "tasks": "...",
  "meetings": "...",
  "documents": "..."
}
```

**Step 4: Upsert Logic**
```python
def upsert_record(database_id, postgres_record):
    """Match by external_id, fallback to (name + subsystem)"""

    # Try to find existing by external_id
    filter_by_id = {
        "property": "External ID",
        "rich_text": {"equals": postgres_record['id']}
    }
    existing = query_database_filtered(database_id, filter_by_id)

    if existing:
        # Update existing
        page_id = existing[0]['id']
        update_page(page_id, map_properties(postgres_record))
        return 'updated'
    else:
        # Fallback: try (name + subsystem)
        filter_by_name = {
            "and": [
                {"property": "Name", "title": {"equals": postgres_record['name']}},
                {"property": "Subsystem", "select": {"equals": postgres_record['subsystem']}}
            ]
        }
        existing = query_database_filtered(database_id, filter_by_name)

        if existing:
            page_id = existing[0]['id']
            update_page(page_id, map_properties(postgres_record))
            return 'updated'
        else:
            # Create new
            create_page(database_id, map_properties(postgres_record))
            return 'created'
```

**Step 5: Document Sync**
```python
def sync_documents(postgres_documents, notion_db_id):
    """Normalize file metadata to Notion"""
    for doc in postgres_documents:
        properties = {
            "Name": {"title": [{"text": {"content": doc['title']}}]},
            "URL": {"url": doc['url']},
            "Category": {"select": {"name": doc['category']}},
            "Subsystem": {"select": {"name": doc['subsystem']}}
        }
        upsert_record(notion_db_id, doc)
```

**Step 6: Validation**
```python
def validate_sync(page_id):
    """Ensure no structural dashboard changes"""
    before_blocks = get_block_children(page_id)
    before_count = len(before_blocks)

    # ... perform sync ...

    after_blocks = get_block_children(page_id)
    after_count = len(after_blocks)

    assert before_count == after_count, "Dashboard structure changed!"
```

**Step 7: Summary Report**
```python
def generate_report(results):
    """Return counts of created/updated records"""
    report = {}
    for table, actions in results.items():
        report[table] = {
            'created': actions.count('created'),
            'updated': actions.count('updated')
        }
    return report

# Example output:
{
  "people": {"created": 10, "updated": 20},
  "tasks": {"created": 150, "updated": 130}
}
```

---

## Rate Limiting

### Notion Rate Limits

**Limits:**
- **3 requests per second** per integration
- **Burst:** Can exceed briefly, then throttled

**Best Practices:**
```python
import time

def rate_limited_request(url, method='GET', **kwargs):
    """Automatically rate limit requests"""
    response = requests.request(method, url, **kwargs)

    # Check for rate limit header
    if 'Retry-After' in response.headers:
        wait_seconds = int(response.headers['Retry-After'])
        print(f"Rate limited. Waiting {wait_seconds}s...")
        time.sleep(wait_seconds)
        return rate_limited_request(url, method, **kwargs)

    # General rate limiting (3 req/sec = 0.33s between requests)
    time.sleep(0.34)
    return response
```

**Batch Processing:**
```python
def sync_records_batched(records, database_id, batch_size=100):
    """Process records in batches with delays"""
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]

        for record in batch:
            upsert_record(database_id, record)
            time.sleep(0.34)  # 3 req/sec

        print(f"Processed batch {i//batch_size + 1}")
        time.sleep(1)  # Extra delay between batches
```

---

## Error Handling

### Common Errors

**1. Invalid Request (400)**
```json
{
  "object": "error",
  "status": 400,
  "code": "validation_error",
  "message": "body.properties.Status.select.name should be one of ..."
}
```

**Fix:** Check property values match database schema

**2. Unauthorized (401)**
```json
{
  "object": "error",
  "status": 401,
  "code": "unauthorized",
  "message": "API token is invalid."
}
```

**Fix:** Verify NOTION_TOKEN is correct and not expired

**3. Object Not Found (404)**
```json
{
  "object": "error",
  "status": 404,
  "code": "object_not_found",
  "message": "Could not find database with ID: ..."
}
```

**Fix:** Verify database ID and integration has access

**4. Rate Limited (429)**
```json
{
  "object": "error",
  "status": 429,
  "code": "rate_limited",
  "message": "Rate limit exceeded"
}
```

**Fix:** Implement exponential backoff

---

### Error Handling Pattern

```python
def safe_notion_request(url, method='GET', **kwargs):
    """Wrapper with error handling"""
    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                # Rate limited
                wait = int(e.response.headers.get('Retry-After', retry_delay))
                print(f"Rate limited, waiting {wait}s...")
                time.sleep(wait)
                retry_delay *= 2  # Exponential backoff
                continue

            elif e.response.status_code in [400, 404]:
                # Client error, don't retry
                print(f"Error: {e.response.json()}")
                raise

            else:
                # Server error, retry
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                raise

        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            raise

    raise Exception(f"Failed after {max_retries} attempts")
```

---

## Examples

### Complete Example: Sync People Table

```python
import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

def sync_people_to_notion():
    """Complete example: Sync people table to Notion"""

    # Step 1: Get Postgres data
    from shared.database.cadence_models import PeopleModel
    people = PeopleModel.query.all()
    print(f"Found {len(people)} people in Postgres")

    # Step 2: Get Notion database ID
    with open('notion_database_ids.json') as f:
        db_ids = json.load(f)
    notion_db_id = db_ids['people']

    # Step 3: Sync each person
    results = []
    for person in people:
        # Map Postgres fields to Notion properties
        properties = {
            "Name": {
                "title": [{"text": {"content": person.name}}]
            },
            "Role": {
                "select": {"name": person.role}
            },
            "Email": {
                "email": person.email
            },
            "Subsystem": {
                "select": {"name": person.subsystem}}
            },
            "External ID": {
                "rich_text": [{"text": {"content": person.person_id}}]
            }
        }

        # Try to find existing
        filter_query = {
            "property": "External ID",
            "rich_text": {"equals": person.person_id}
        }
        url = f'https://api.notion.com/v1/databases/{notion_db_id}/query'
        response = requests.post(url, headers=HEADERS, json={"filter": filter_query})
        existing = response.json()['results']

        if existing:
            # Update
            page_id = existing[0]['id']
            url = f'https://api.notion.com/v1/pages/{page_id}'
            response = requests.patch(url, headers=HEADERS, json={"properties": properties})
            results.append('updated')
        else:
            # Create
            url = 'https://api.notion.com/v1/pages'
            payload = {
                "parent": {"database_id": notion_db_id},
                "properties": properties
            }
            response = requests.post(url, headers=HEADERS, json=payload)
            results.append('created')

        time.sleep(0.34)  # Rate limiting

    # Step 4: Report
    print(f"Created: {results.count('created')}")
    print(f"Updated: {results.count('updated')}")

if __name__ == "__main__":
    sync_people_to_notion()
```

---

## Database IDs Reference

**FRAMES Notion Databases:**

```json
{
  "module_library": "eac1ce58-6169-4dc3-a821-29858ae59e76",
  "launch_readiness": "2b96b8ea-578a-81ce-a84d-cba10098f012",
  "team_directory": "2b96b8ea-578a-8165-905e-d8d01c403cc2",
  "development_tasks": "662cbb0c-1cca-4c12-9991-c566f220eb0c",
  "technical_decisions": "48623dd2-4f8a-4226-be4c-6e7255abbf7e",
  "integration_checklist": "ebe41b52-7903-461d-8fb9-18dc16ae9bdc"
}
```

**CADENCE Proto-type Page:**
```
Page ID: 2b86b8ea-578a-80cb-8f25-f080444ec266
```

---

## Resources

- [Notion API Documentation](https://developers.notion.com/)
- [API Reference](https://developers.notion.com/reference/intro)
- [Property Values](https://developers.notion.com/reference/property-value-object)
- [Rate Limits](https://developers.notion.com/reference/request-limits)

---

**Last Updated:** 2025-11-28
**Maintained By:** Agent Beta
**API Version:** 2022-06-28
**Questions:** See [CADENCE Spec Compliance](CADENCE_SPEC_COMPLIANCE.md) for behavior rules
