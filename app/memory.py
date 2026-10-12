from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import MemoryEntry

def add_memory(db: Session, contact_key: str, content: str, source: str = "manual"):
    row = MemoryEntry(contact_key=contact_key.strip().lower(), content=content.strip(), source=source)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

def get_memories(db: Session, contact_key: str, limit: int = 20):
    stmt = select(MemoryEntry).where(MemoryEntry.contact_key == contact_key.strip().lower()).order_by(MemoryEntry.id.desc()).limit(limit)
    return list(db.scalars(stmt).all())

def seed_demo_memories(db: Session):
    if db.query(MemoryEntry).count() == 0:
        add_memory(db, "alex@acme.example", "Prefers concise status updates; usually available Tuesday or Thursday.", "demo_seed")
        add_memory(db, "priya@acme.example", "Architecture reviews should include agenda, risks, and owner for each action.", "demo_seed")
        add_memory(db, "sam@acme.example", "Interested in practical agent orchestration and evaluation.", "demo_seed")
