from fastapi import FastAPI

app = FastAPI()


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck():
    return {"ok": True}
