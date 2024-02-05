from fastapi import FastAPI
from fastapi.routing import APIRoute

from main import app


def get_route(app: FastAPI, name: str) -> APIRoute:
    results = [
        route
        for route in app.routes
        if isinstance(route, APIRoute) and route.name == name
    ]
    if not results:
        raise KeyError(f'No GET route registered with name: {name}')
    return results[0]


def reverse_url(path: str, **kwargs) -> str:
    return get_route(app, path).path.format(**kwargs)
