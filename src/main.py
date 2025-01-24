from fastapi import FastAPI, routing
import uvicorn
from routes import base, summary

app = FastAPI()

app.include_router(base.base_router)
app.include_router(summary.summ_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
