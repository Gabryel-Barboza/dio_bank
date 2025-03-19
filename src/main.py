from contextlib import asynccontextmanager

from fastapi import FastAPI

from .controllers import user_controller
from .databases.bank_db import create_db


# Database and other configs
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


# App Instance
def create_app():
    app = FastAPI(
        title='DIO Bank API',
        summary='API to make transactional requests, also manipulate users and accounts.',
        version='0.0.2',
        description="""

    """,
        openapi_tags='',
        openapi_url='/doc',  # /docs - Swagger, /redoc
        lifespan=lifespan,
    )

    app.include_router(user_controller.router)

    return app
