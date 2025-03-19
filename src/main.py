from fastapi import FastAPI

from .controllers import user_controller


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
    )

    app.include_router(user_controller.router)

    return app
