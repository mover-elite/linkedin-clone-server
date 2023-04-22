from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse

from app.api.main_router import router as main_router
from app.schemas.error import ValidationError

from app.core.config import settings

app = FastAPI(
    title=settings.TITLE,
    responses={422: {"description": "Validation Error", "model": ValidationError}},
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, e):
    errors = []
    for error in e.errors():
        error_obj = {"path": error["loc"][1], "msg": error["msg"]}
        errors.append(error_obj)
    return JSONResponse(content={"errors": errors}, status_code=422)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse("/docs")


app.include_router(main_router)
