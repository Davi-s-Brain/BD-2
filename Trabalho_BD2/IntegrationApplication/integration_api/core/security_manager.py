from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from integration_api.core.secret_manager import SecretManager

class SecurityManager:
    def __init__(self):
        self.secret_manager = SecretManager()

    def validate(self, request: Request):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")

        api_key = token.removeprefix("Bearer ").strip()
        expected_key = self.secret_manager.get_secret("API_KEY")
        if api_key != expected_key:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")
