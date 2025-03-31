from contextlib import asynccontextmanager

from fastapi import FastAPI

from .controllers import account_controller, auth_controller, user_controller
from .databases.bank_db import create_db


# Database and other configs
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


# App Instance
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
app.include_router(account_controller.router)
app.include_router(auth_controller.router)

# Run with fastapi dev src/main.py
# or uvicorn src.main:app --reload
