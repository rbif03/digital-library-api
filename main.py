from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from db.core import DatabaseError, ForeignKeyError, NotFoundError
from routers.authors import router as author_router
from routers.books import router as book_router


app = FastAPI()


@app.exception_handler(DatabaseError)
def handle_database_error(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": f"Failed to execute database operation. {exc}",
            "data": None,
        },
    )


@app.exception_handler(NotFoundError)
def handle_not_found_error(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": f"Failed find requested item. {exc}",
            "data": None,
        },
    )


@app.exception_handler(ForeignKeyError)
def handle_not_found_error(request: Request, exc: ForeignKeyError):
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": f"Foreign Key passed does not exist in parent table. {exc}",
            "data": None,
        },
    )


app.include_router(author_router)
app.include_router(book_router)
