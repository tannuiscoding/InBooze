import os
import json
from mindsdb_sdk import Client
from datetime import datetime

MINDSDB_API = os.getenv('MINDSDB_API', 'http://127.0.0.1:47334') 
client = Client(api_url=MINDSDB_API)


KB_NAME = 'email_kb'
if KB_NAME not in [kb.name for kb in client.knowledge_bases.list()]:
    kb = client.knowledge_bases.create(KB_NAME)
else:
    kb = client.knowledge_bases.get(KB_NAME)


sample_emails = [
    {
        "sender": "john@client.com",
        "date": "2025-06-09",
        "subject": "Delivery delay update",
        "labels": ["client", "delay"],
        "is_read": False,
        "content": "Hi, due to unforeseen issues, your order is delayed by 2 days."
    },
    {
        "sender": "projectx@company.com",
        "date": "2025-06-08",
        "subject": "Project Apollo Plan",
        "labels": ["project", "apollo"],
        "is_read": True,
        "content": "Here is the final plan for Project Apollo with milestone updates."
    }
]

def ingest_emails(email_data):
    for email in email_data:
        kb.insert(
            content=email['content'],
            metadata={
                'sender': email['sender'],
                'date': email['date'],
                'subject': email['subject'],
                'labels': ','.join(email['labels']),
                'is_read': email['is_read']
            }
        )


def create_index():
    client.query(
        f"CREATE INDEX ON KNOWLEDGE_BASE {KB_NAME};"
    )


def search_emails(query):
    results = client.query(
        f"SELECT * FROM {KB_NAME} WHERE content LIKE '{query}' AND metadata->'is_read' = false"
    )
    return results

if __name__ == '__main__':
    print("Ingesting emails...")
    ingest_emails(sample_emails)
    print("Creating index...")
    create_index()
    print("Running test query...")
    res = search_emails("emails from clients about delays")
    for row in res:
        print(json.dumps(row, indent=2))
