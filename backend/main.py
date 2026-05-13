from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.manager.v1.router import router
from src.config.session import engine
from src.models.mixins.base import BaseMixin


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(BaseMixin.metadata.create_all)

    yield
    print("Application shutdown")


app = FastAPI(
    title="Inventory API",
    description="API para gerenciamento de produtos e pedidos",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    tags=["Health"],
)
def health_check():
    return {
        "status": "ok",
    }


# API Routes
app.include_router(
    router,
    prefix="/api",
)
