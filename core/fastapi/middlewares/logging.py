import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response

class LoggingMiddleware(BaseHTTPMiddleware):
    def _init__(self, app):
        super()._init__(app)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
    )