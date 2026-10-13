from app.integrations import fetch_unified_inbox
from app.memory import get_memories

def build_reply(db, message_id: str, tone: str = "professional", extra_context: str = ""):
    message = next((m for m in fetch_unified_inbox() if m["id"] == message_id), None)
    if not message:
        raise ValueError("Message not found. Use GET /api/inbox to list demo messages.")
    memories = get_memories(db, message["contact_key"])
    context = [m.content for m in memories]
    if extra_context.strip():
        context.append(extra_context.strip())
    style = {
        "professional": "Thanks for reaching out.",
        "concise": "Thanks —",
        "friendly": "Hi, thanks for the note!",
    }.get(tone.lower(), "Thanks for reaching out.")
    details = " ".join(context[:2])
    if message["provider"] == "gmail":
        body = "I can confirm the review for next week. I'll share a short status update and flag any blockers beforehand."
    elif message["provider"] == "google_calendar":
        body = "I'll send an agenda covering architecture decisions, key risks, and action owners ahead of the review."
    else:
        body = "I'd be glad to compare notes. I'll follow up with a few practical examples of agent workflows."
    if tone.lower() == "concise":
        body = body.split(".")[0] + "."
    draft = f"{style}\n\n{body}"
    if details:
        draft += f"\n\n(Context considered: {details})"
    return {"message_id": message_id, "contact_key": message["contact_key"], "context_used": context, "draft": draft}
