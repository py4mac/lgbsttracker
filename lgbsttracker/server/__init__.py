from aiohttp import web


def _get_api_storage_sensors_server():
    from lgbsttracker.server.endpoints.storage_sensors import init, get_endpoints

    init()

    app = web.Application()
    # Register route
    for http_path, handler, method in get_endpoints():
        app.router.add_route(method, http_path, handler)
    return app


def _get_api_doc_server():
    app = web.Application()

    def index(request):
        return web.FileResponse("./lgbsttracker/server/doc/index.html")

    def swagger_serve(request):
        return web.FileResponse("./lgbsttracker/server/doc/swagger.json")

    # def logo_serve(request):
    #     return web.FileResponse("./lgbsttracker/server/doc/logo.png")

    # Specific route
    app.router.add_route("*", "/", index)
    app.router.add_route("*", "/swagger.json", swagger_serve)
    # app.router.add_route("*", "/logo.png", logo_serve)
    return app


def _run_server(app):
    web.run_app(app, host="0.0.0.0", port=8000)
