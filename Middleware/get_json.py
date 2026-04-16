from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class JSONMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                request.state.json_data = await request.json()
            except:
                request.state.json_data = {}
        else:
            request.state.json_data = {}
        response = await call_next(request)
        return response
