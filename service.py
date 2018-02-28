from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime


class Service:
    def __init__(self, uri, db_name):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    async def find(self, start, end, page):
        since = datetime(1970, 1, 1, 0, 0, 0)
        begin = (datetime.strptime(start, '%Y-%m-%d') - since).total_seconds()
        to = (datetime.strptime(end, '%Y-%m-%d') - since).total_seconds()
        query = {"time": {"$gte": int(begin), "$lt": int(to)}}
        print(query)

        docs = await self.db.orders.find(query).skip(16*(page-1)).limit(16).to_list(length=16)
        for doc in docs:
            del doc['id']
            del doc['name']
            del doc['payOption']
            del doc['milliseconds']
            del doc['_id']
            del doc['month']
            del doc['status']
            del doc['timestamp']
            del doc['userId']
            del doc['year']

        return docs
