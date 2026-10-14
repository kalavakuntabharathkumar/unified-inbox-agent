from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.config import settings
from app.database import Base, engine, get_db
from app.models import MemoryEntry
from app.schemas import DraftRequest, MemoryCreate
from app.integrations import fetch_unified_inbox, send_telegram_message
from app.memory import add_memory, get_memories, seed_demo_memories
from app.agent import build_reply

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    from app.database import SessionLocal
    with SessionLocal() as db:
        seed_demo_memories(db)
    yield

app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
def home():
    return '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Unified Inbox Agent</title><style>
    body{margin:0;background:#0b1020;color:#e8edf8;font:15px system-ui}header{padding:28px 5vw;background:#121a30;border-bottom:1px solid #26314d}
    h1{margin:0;font-size:28px}p{color:#aebbd4}.wrap{max-width:1100px;margin:auto;padding:24px 5vw}.grid{display:grid;grid-template-columns:1.2fr 1fr;gap:18px}
    .card{background:#121a30;border:1px solid #26314d;border-radius:16px;padding:20px}.item{padding:14px 0;border-bottom:1px solid #26314d}
    button{background:#7c9cff;color:#071126;border:0;border-radius:9px;padding:10px 14px;font-weight:700;cursor:pointer}input,textarea,select{width:100%;box-sizing:border-box;background:#0b1020;color:#e8edf8;border:1px solid #344260;border-radius:8px;padding:10px;margin:6px 0 12px}
    pre{white-space:pre-wrap;overflow-wrap:anywhere;color:#d6e0f8}@media(max-width:760px){.grid{grid-template-columns:1fr}}</style></head><body>
    <header><h1>Unified Inbox Agent</h1><p>Gmail · Calendar · LinkedIn · Persistent contact memory</p></header><main class="wrap"><div class="grid">
    <section class="card"><h2>Unified inbox</h2><div id="inbox">Loading messages…</div></section>
    <section class="card"><h2>Draft a reply</h2><label>Message ID</label><input id="messageId" value="gmail-101"><label>Tone</label><select id="tone"><option>professional</option><option>concise</option><option>friendly</option></select><label>Additional context</label><textarea id="extra" rows="3" placeholder="Optional context"></textarea><button onclick="draft()">Generate draft</button><pre id="draft"></pre>
    <h2>Add contact memory</h2><input id="contact" placeholder="contact email"><textarea id="memory" rows="2" placeholder="Useful context"></textarea><button onclick="saveMemory()">Save memory</button><p id="saved"></p></section></div></main>
    <script>
    async function load(){let r=await fetch('/api/inbox'),d=await r.json();document.getElementById('inbox').innerHTML=d.map(m=>`<div class="item"><b>${m.sender}</b> <small>· ${m.provider}</small><p>${m.subject}</p><p>${m.body}</p><button onclick="document.getElementById('messageId').value='${m.id}'">Draft reply</button></div>`).join('')}
    async function draft(){let r=await fetch('/api/draft',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message_id:document.getElementById('messageId').value,tone:document.getElementById('tone').value,extra_context:document.getElementById('extra').value})});let d=await r.json();document.getElementById('draft').textContent=d.draft||d.detail}
    async function saveMemory(){let r=await fetch('/api/memory',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({contact_key:document.getElementById('contact').value,content:document.getElementById('memory').value,source:'ui'})});document.getElementById('saved').textContent=r.ok?'Memory saved.':'Could not save memory.'}
    load();
    </script></body></html>'''

@app.get("/api/health")
def health():
    return {"status": "ok", "demo_mode": settings.demo_mode, "database": "configured"}

@app.get("/api/inbox")
def inbox():
    return fetch_unified_inbox()

@app.post("/api/draft")
def draft_reply(payload: DraftRequest, db: Session = Depends(get_db)):
    try:
        return build_reply(db, payload.message_id, payload.tone, payload.extra_context)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@app.post("/api/memory")
def create_memory(payload: MemoryCreate, db: Session = Depends(get_db)):
    row = add_memory(db, payload.contact_key, payload.content, payload.source)
    return {"id": row.id, "contact_key": row.contact_key, "content": row.content, "source": row.source}

@app.get("/api/memory/{contact_key:path}")
def read_memory(contact_key: str, db: Session = Depends(get_db)):
    return [{"id": m.id, "contact_key": m.contact_key, "content": m.content, "source": m.source, "created_at": m.created_at.isoformat()} for m in get_memories(db, contact_key)]

@app.post("/api/telegram/webhook")
def telegram_webhook(update: dict, db: Session = Depends(get_db)):
    message = update.get("message", {})
    chat_id = str(message.get("chat", {}).get("id", "demo-chat"))
    text = message.get("text", "")
    reply = "Unified Inbox Agent demo is active. Send /help for commands."
    if text.startswith("/draft"):
        result = build_reply(db, "gmail-101", "professional", text.replace("/draft", "", 1).strip())
        reply = result["draft"]
    elif text.startswith("/help"):
        reply = "Commands: /help, /draft [extra context]. Demo mode does not send messages externally."
    return send_telegram_message(chat_id, reply)
