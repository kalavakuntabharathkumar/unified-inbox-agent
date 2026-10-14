from app.agent import build_reply
from app.database import Base, engine, SessionLocal
from app.memory import add_memory

def test_reply_uses_contact_memory():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        add_memory(db, "alex@acme.example", "Likes concise updates", "test")
        result = build_reply(db, "gmail-101", "professional")
        assert result["contact_key"] == "alex@acme.example"
        assert "concise updates" in " ".join(result["context_used"])

def test_unknown_message_raises():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        try:
            build_reply(db, "unknown")
            assert False, "Expected ValueError"
        except ValueError:
            pass
