from fastapi import FastAPI

app = FastAPI(
    title="Weather App Backend",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Weather App Backend is running"}