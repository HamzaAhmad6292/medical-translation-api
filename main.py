from fastapi import FastAPI
from app.routers.translation import router as translation_router
from app.config.settings import settings
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Medical Translation API")

# Include routers
app.include_router(translation_router)
# Add to your FastAPI app initialization


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify the front end origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)