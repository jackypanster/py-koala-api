from sanic import Sanic
from sanic.response import json
from sanic.exceptions import ServerError
import logging

logging.basicConfig(filename='log/koala.log', level=logging.INFO)

app = Sanic()
app.config.from_envvar('APP_SETTINGS')
print(app.config)


@app.listener('before_server_start')
async def setup_db(app, loop):
    print('db setup')


@app.listener('after_server_start')
async def notify_server_started(app, loop):
    print('Server successfully started!')


@app.listener('before_server_stop')
async def notify_server_stopping(app, loop):
    print('Server shutting down!')


@app.listener('after_server_stop')
async def close_db(app, loop):
    print('db close')


@app.middleware('request')
async def print_on_request(request):
    print("I print when a request is received by the server")


@app.middleware('response')
async def prevent_xss(request, response):
    response.headers["x-xss-protection"] = "1; mode=block"


@app.get("/orders/<start:string>/<end:string>/<page:int>")
async def order_by_duration(request, start, end, page):
    return json({"hello": "1"})


@app.get("/orders/<user:string>/<start:string>/<end:string>/<page:int>")
async def order_by_user(request, user, start, end, page):
    return json({"hello": "2"})


@app.get("/orders/<date:string>/<page:int>")
async def order_by_date(request, date, page):
    return json({"hello": "3"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, workers=app.config.WORKERS,
            debug=app.config.DEBUG, access_log=app.config.DEBUG)
