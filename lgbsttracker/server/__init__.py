from sanic import Sanic
from sanic.response import file
from lgbsttracker.server.handlers import get_endpoints

app = Sanic(__name__)

for http_path, handler, methods in get_endpoints():
    app.add_route(uri=http_path, handler=handler, methods=methods)


@app.route("/swagger.json")
def home(response):
    return file("./lgbsttracker/server/doc/swagger.json")


@app.route("/")
def home(response):
    return file("./lgbsttracker/server/doc/index.html")


def _run_server():
    app.run(host="0.0.0.0", port=8000)
