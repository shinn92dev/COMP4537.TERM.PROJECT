# This code was developed with the assistance of ChatGPT.

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response
from crud import DBController
from models import APIKey, APIUsage, HTTPMethodEnum

db_controller = DBController()

class UsageMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path
        method_str = request.method
        api_key = request.headers.get("api_key")

        response: Response = await call_next(request)

        if api_key:
            try:
                db_session = next(db_controller.get_db())

                record = db_session.query(APIKey).filter(APIKey.key == api_key).first()
                if record:
                    method_enum = None
                    if method_str in HTTPMethodEnum._value2member_map_:
                        method_enum = HTTPMethodEnum(method_str)

                    usage_obj = APIUsage(
                        key_id = record.key_id,
                        count=1,
                        method=method_enum,
                        endpoint=path
                    )
                    db_session.add(usage_obj)
                    db_session.commit()
                    db_session.refresh(usage_obj)
            except Exception as e:
                print(f"[UsageMiddleware Error] Failed to log usage: {e}")
            finally:
                db_session.close()
        return response