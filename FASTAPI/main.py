from fastapi import FastAPI
from routers import trabajadores, feedbacks

app = FastAPI()

app.include_router(trabajadores.router)
app.include_router(feedbacks.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
