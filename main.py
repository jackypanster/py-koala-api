from sanic import Sanic
from sanic.response import json
from sanic.exceptions import ServerError
from datetime import datetime
import logging

logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
logging_format += "%(message)s"

logging.basicConfig(
    filename='log/koala.log',
    format=logging_format,
    level=logging.DEBUG
)
log = logging.getLogger()

app = Sanic(__name__)
app.config.from_envvar('APP_SETTINGS')
log.debug(app.config)


@app.listener('before_server_start')
def init(sanic, loop):
    global db
    from motor.motor_asyncio import AsyncIOMotorClient
    mongo_uri = app.config.MONGO_URL
    db = app.config.DB
    db = AsyncIOMotorClient(mongo_uri)['test']
    log.debug(db)


@app.middleware('request')
async def print_on_request(request):
    log.debug(request)


@app.middleware('response')
async def prevent_xss(request, response):
    response.headers["x-xss-protection"] = "1; mode=block"


@app.get("/stat/order/list/<start:string>/<end:string>/<page:int>")
async def order_by_duration(request, start, end, page):
    since = datetime(1970, 1, 1, 0, 0, 0)
    begin = (datetime.strptime(start, '%Y-%m-%d') - since).total_seconds()
    to = (datetime.strptime(end, '%Y-%m-%d') - since).total_seconds()
    query = {"time": {"$gte": int(begin), "$lt": int(to)}}
    log.debug(query)
    # docs = await db.orders.find(query).skip(16*(page-1)).limit(16)
    docs = await db.orders.find({}).to_list(length=100)
    return json(docs)


@app.get("/orders/<user:string>/<start:string>/<end:string>/<page:int>")
async def order_by_user(request, user, start, end, page):
    return json({"hello": "2"})


@app.get("/orders/<date:string>/<page:int>")
async def order_by_date(request, date, page):
    pass


@app.route('/objects', methods=['GET'])
async def get(request):
    docs = await db.test_col.find().to_list(length=100)
    for doc in docs:
        doc['id'] = str(doc['_id'])
        del doc['_id']
    return json(docs)


@app.route('/post', methods=['POST'])
async def new(request):
    doc = request.json
    print(doc)
    object_id = await db.test_col.save(doc)
    return json({'object_id': str(object_id)})


@app.get("/ping")
async def ping(request):
    return json({"message": "pong"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, workers=app.config.WORKERS,
            debug=app.config.DEBUG, access_log=app.config.DEBUG)
