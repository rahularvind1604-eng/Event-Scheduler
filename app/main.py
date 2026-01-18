from fastapi import FastAPI

app=FastAPI(title="Event Sceduler")

@app.get("/health")
def health():
    return {"status":"ok"}
