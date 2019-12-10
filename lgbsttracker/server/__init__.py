import uvicorn
# from aiohttp import web
from fastapi import FastAPI
from lgbsttracker.server.handlers import get_endpoints

app = FastAPI(debug=True)

for http_path, handler, methods in get_endpoints():
    app.add_api_route(path=http_path, endpoint=handler, methods=methods)


def _run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# def create_app():
#     import handlers

#     app = web.Application()
#     for http_path, handler, methods in handlers.get_endpoints():
#         app.router.add_route(methods[0], http_path, handler)
#     return app

# async def async_create_app():
#     import asyncio

#     return await asyncio.coroutine(create_app)()

# if __name__ == "__main__":
#     app = create_app()
#     web.run_app(app, host='0.0.0.0', port=8000)
