from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse

from application.api.endpoints import todos, users
from application.api.middleware.middleware import logging_middleware, logger
from application.core.security import get_user_by_valid_token

application = FastAPI()

application.include_router(todos.router, prefix="/api/v1", tags=["Todos"],
                           dependencies=[Depends(get_user_by_valid_token)])
application.include_router(users.router, prefix="/api/v1", tags=["Users"])

application.middleware("http")(logging_middleware)


@application.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Exception occurred!")
    return JSONResponse(
        status_code=500, content={"error": "Internal server error"}
    )


@application.get("/")
def read_root():
    return {"message": "Welcome to simple TODO API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(application, host="127.0.0.1", port=8000)
