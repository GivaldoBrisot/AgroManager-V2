from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from config import ALLOWED_ORIGINS

# Import rotas
from routes import romaneios, fazendas, talhoes, safras, cereais, caminhoes, empresas
from routes.auth import router as auth_router

# Cria aplicação FastAPI
app = FastAPI(
    title="AgroManager API",
    description="API para gerenciamento agrícola com cálculos de romaneios",
    version="2.0.0"
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui rotas de API
app.include_router(auth_router)
app.include_router(romaneios.router)
app.include_router(fazendas.router)
app.include_router(talhoes.router)
app.include_router(safras.router)
app.include_router(cereais.router)
app.include_router(caminhoes.router)
app.include_router(empresas.router)

# Serve arquivos estáticos (frontend)
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path, html=True), name="static")

@app.get("/")
async def root():
    """Página raiz - redireciona para frontend"""
    frontend_index = os.path.join(frontend_path, "index.html")
    if os.path.exists(frontend_index):
        return FileResponse(frontend_index)
    return {"message": "AgroManager API v2.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/docs")
async def swagger_docs():
    """Documentação interativa (Swagger)"""
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
