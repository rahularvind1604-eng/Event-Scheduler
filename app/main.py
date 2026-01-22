from fastapi import FastAPI
from app.api.routes import router as admin_router

app=FastAPI(title="Event Sceduler")

@app.get("/health")
def health():
    return {"status":"ok"}
app.include_router(admin_router)