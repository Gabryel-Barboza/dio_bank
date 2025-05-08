from contextlib import asynccontextmanager

from fastapi import FastAPI

from .controllers import account_controller, auth_controller, user_controller
from .databases.bank_db import connect_db
from .exception_handler import ExceptionHandlingMiddleware


# Database and other configs
@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_db()
    yield


# App Instance
app = FastAPI(
    title='DIO Bank API',
    summary='API to make transactional requests, also manipulate users and accounts.',
    version='0.1.0',
    description="""

""",
    openapi_tags='',
    openapi_url='/doc',  # /docs - Swagger, /redoc
    lifespan=lifespan,
)

# Routing

app.include_router(user_controller.router)
app.include_router(account_controller.router)
app.include_router(auth_controller.router)

# App run with fastapi dev src/main.py or
# uvicorn src.main:app --reload [--lifespan on # debug de lifespan]

# Middlewares para tratar problemas antes e depois de uma request
app.add_middleware(ExceptionHandlingMiddleware)
