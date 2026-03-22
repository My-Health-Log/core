from fastapi import Request

from app.services.provider import ExtractionProvider


def get_provider(request: Request) -> ExtractionProvider:
    return request.app.state.provider
