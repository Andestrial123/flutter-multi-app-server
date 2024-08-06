import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.config import config, postgres_config
from app.endpoints import metadata
from app.endpoints.v1 import router_v1
from app.models.db import db
from app.models.db.migrations.upgrade import run_async_upgrade

app = FastAPI(
    title='Multi App API',
    description='Multi App Service',
    version=config.version,
    openapi_tags=metadata.TAGS,
    openapi_url="/multi/resource/openapi.json",
    docs_url='/multi/docs',
    redoc_url='/multi/redoc',
    debug=config.debug,
)

app.include_router(router=router_v1)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def exception_handler(request: Request, call_next):
    body = await request.body()

    try:
        return await call_next(request)

    except Exception as ex:
        logger = logging.getLogger(__name__)
        logger.exception(f"Exception: {request.method} {request.url}, body: {body} -> [{ex}]")

        return JSONResponse(
            status_code=500,
            content={
                "detail": f"Internal Server Error",
            },
        )


@app.on_event("startup")
async def start():
    db.setup(postgres_config)
    await run_async_upgrade()


@app.get("/health", tags=["Internal"])
async def root():
    return {
        "version": config.version,
        "status": "Ok",
    }
