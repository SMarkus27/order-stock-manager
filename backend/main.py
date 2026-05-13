from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.manager.v1.exceptions import ApiException
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


@app.exception_handler(ApiException)
async def api_exception_handler(request: Request, exc: ApiException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
        },
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
