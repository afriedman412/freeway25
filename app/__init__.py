import os
from fastapi import FastAPI


def generate_app() -> FastAPI:
    app = FastAPI()
    if not os.getenv("PRO_PUBLICA_API_KEY"):
        from dotenv import load_dotenv
        load_dotenv()
    assert os.getenv("PRO_PUBLICA_API_KEY") is not None
    return app
