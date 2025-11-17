import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

from database import create_document, get_documents
from schemas import RecoveryRequest, ContactMessage

app = FastAPI(title="Coins Guard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Coins Guard Backend läuft"}

@app.get("/api/hello")
def hello() -> Dict[str, str]:
    return {"message": "Willkommen bei Coins Guard"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = getattr(db, 'name', '✅ Connected')
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# Coins Guard endpoints
@app.post("/api/recovery")
def create_recovery_request(payload: RecoveryRequest) -> Dict[str, Any]:
    try:
        inserted_id = create_document("recoveryrequest", payload)
        return {"status": "ok", "id": inserted_id, "message": "Anfrage erhalten. Unser Team meldet sich."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact")
def create_contact_message(payload: ContactMessage) -> Dict[str, Any]:
    try:
        inserted_id = create_document("contactmessage", payload)
        return {"status": "ok", "id": inserted_id, "message": "Nachricht gesendet. Wir antworten zeitnah."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recovery")
def list_recent_recovery(limit: int = 5):
    try:
        docs = get_documents("recoveryrequest", {}, limit)
        # Sanitize ObjectId for JSON if present
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
