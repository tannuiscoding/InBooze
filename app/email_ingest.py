import mailbox
import os
from datetime import datetime
from mindsdb_sdk import connect

MINDSDB_URL = os.getenv("MINDSDB_URL", "http://127.0.0.1:47334")
KB_NAME = "inbooze_kb"

conn = connect(MINDSDB_URL)

def process_mbox_and_insert(filepath):
    try:
        mbox = mailbox.mbox(filepath)
        rows = []
        for msg in mbox:
            try:
                content = msg.get_payload(decode=True)
                if isinstance(content, bytes):
                    content = content.decode(errors='ignore')

                sender = msg.get("From", "")
                subject = msg.get("Subject", "")
                date = msg.get("Date", "")
                iso_date = datetime.strptime(date[:25], "%a, %d %b %Y %H:%M:%S").isoformat() if date else None

                row = {
                    "content": content.strip(),
                    "metadata": {
                        "sender": sender,
                        "subject": subject,
                        "date": iso_date
                    }
                }
                rows.append(row)
            except Exception as inner_e:
                print(f"[mbox email skipped] {inner_e}")

        print(f"[Ingest] Parsed {len(rows)} emails. Uploading...")

        conn.sql(f"""
            CREATE KNOWLEDGE_BASE IF NOT EXISTS {KB_NAME} (
                content TEXT,
                metadata COLUMNS(sender TEXT, subject TEXT, date TEXT)
            )
        """)

        conn.sql(f"CREATE INDEX IF NOT EXISTS ON KNOWLEDGE_BASE {KB_NAME} (content)")

        for r in rows:
            conn.sql(f"""
                INSERT INTO {KB_NAME} (
                    content,
                    metadata.sender,
                    metadata.subject,
                    metadata.date
                ) VALUES (
                    %(content)s,
                    %(metadata.sender)s,
                    %(metadata.subject)s,
                    %(metadata.date)s
                )
            """, r)

        print(f"[Ingest] Done ingesting {len(rows)} emails into KB '{KB_NAME}'.")

    except Exception as e:
        print(f"[process_mbox_and_insert] Error: {e}")


def parse_and_ingest_mbox(filepath):
    """Compatibility wrapper used by routes. Parses an .mbox and ingests emails."""
    return process_mbox_and_insert(filepath)