from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import analyze

app = FastAPI(
    title="Veridict AI API"
)

# Configuração CORS - Permitir Front-End React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # we must change this to the actual domain in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api/v1") # Router used to isolate and organize API endpoints related to analysis, making the codebase more modular and maintainable.

@app.get("/")
def read_root():
    return {"message": "Welcome to Veridict AI API. Use /api/v1/analyze to analyze content."}
