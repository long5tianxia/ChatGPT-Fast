from fastapi import FastAPI
from app.api.routers import v1
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware


def register_app() -> FastAPI:
    app = FastAPI(
        docs_url=None,
        openapi_url=None
    )
    # 中间件
    register_middleware(app)

    # 路由
    register_router(app)

    return app


def register_middleware(app: FastAPI):
    # cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # gzip
    app.add_middleware(GZipMiddleware)


def register_router(app: FastAPI):
    """
    路由
    :param app: FastAPI
    :return:
    """
    app.include_router(
        v1,
    )
