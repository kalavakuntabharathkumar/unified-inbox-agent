"""Provider boundary. Replace demo methods with authorized Composio/MCP actions."""
from datetime import datetime, timezone, timedelta

def fetch_unified_inbox():
    now = datetime.now(timezone.utc)
    return [
        {"id": "gmail-101", "provider": "gmail", "contact_key": "alex@acme.example",
         "sender": "Alex Morgan", "subject": "Q4 integration timeline",
         "body": "Can we confirm the integration review for next week?", "received_at": (now-timedelta(minutes=18)).isoformat()},
        {"id": "calendar-202", "provider": "google_calendar", "contact_key": "priya@acme.example",
         "sender": "Priya Shah", "subject": "Architecture review invite",
         "body": "Please share a short agenda before the meeting.", "received_at": (now-timedelta(hours=2)).isoformat()},
        {"id": "linkedin-303", "provider": "linkedin", "contact_key": "sam@acme.example",
         "sender": "Sam Lee", "subject": "Connection follow-up",
         "body": "Great connecting. Would be useful to compare notes on agent workflows.", "received_at": (now-timedelta(days=1)).isoformat()},
    ]

def send_telegram_message(chat_id: str, text: str):
    # Demo mode: never sends a real network request.
    return {"ok": True, "demo": True, "chat_id": str(chat_id), "text": text}
