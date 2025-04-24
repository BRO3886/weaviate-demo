from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from app.models.exceptions import InternalServerError, NotFoundError, ValidationError


class GlobalExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            if isinstance(e, ValidationError):
                return JSONResponse(
                    content={"error": str(e)}, status_code=e.status_code
                )
            elif isinstance(e, NotFoundError):
                return JSONResponse(
                    content={"error": str(e)}, status_code=e.status_code
                )
            elif isinstance(e, InternalServerError):
                return JSONResponse(
                    content={"error": str(e)}, status_code=e.status_code
                )
            else:
                return JSONResponse(content={"error": str(e)}, status_code=500)


class StaticFilesHandler(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        if isinstance(response, FileResponse):
            response.headers["X-Content-Type-Options"] = "nosniff"
            if path.endswith((".jpg", ".jpeg")):
                response.headers["Content-Type"] = "image/jpeg"
            elif path.endswith(".png"):
                response.headers["Content-Type"] = "image/png"
            elif path.endswith(".gif"):
                response.headers["Content-Type"] = "image/gif"
            elif path.endswith(".svg"):
                response.headers["Content-Type"] = "image/svg+xml"
        return response
