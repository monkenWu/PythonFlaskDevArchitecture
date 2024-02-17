import os
from dotenv import load_dotenv, find_dotenv

class EnvLoader:
    is_testing = False
    env_loaded = False
    
    @staticmethod
    def getenv(key: str) -> str:
        if not EnvLoader.env_loaded:
            if EnvLoader.is_testing:
                load_dotenv(find_dotenv('.testing.env'), override=True)
            else:
                load_dotenv('.env', override=True)
            EnvLoader.env_loaded = True
        return os.getenv(key)

    @staticmethod
    def setenv(key: str, value: str):
        os.environ[key] = value
        return os.getenv(key)