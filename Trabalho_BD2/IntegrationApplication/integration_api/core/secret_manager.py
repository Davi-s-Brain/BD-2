import os

class SecretManager:
    def __init__(self):
        self._secrets = {
            "API_KEY": os.getenv("API_KEY", "secreta")
        }

    def get_secret(self, key: str) -> str:
        return self._secrets.get(key)
