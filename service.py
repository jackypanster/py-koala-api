from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime


class Service:
    def __init__(self, uri, db_name, log):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.log = log

    async def find(self, start, end, page, pageSize):
        since = datetime(1970, 1, 1, 0, 0, 0)
        begin = (datetime.strptime(start, '%Y-%m-%d') - since).total_seconds()
        to = (datetime.strptime(end, '%Y-%m-%d') - since).total_seconds()
        query = {"time": {"$gte": int(begin), "$lt": int(to)}}
        self.log.debug(query)

        n = await self.db.orders.find(query).count()

        docs = await self.db.orders.find(query).skip(pageSize*(page-1)).limit(pageSize).to_list(length=pageSize)
        for doc in docs:
            if 'id' in doc.keys():
                del doc['id']

            if 'name' in doc.keys():
                del doc['name']

            if 'payOption' in doc.keys():
                del doc['payOption']

            if 'milliseconds' in doc.keys():
                del doc['milliseconds']

            if '_id' in doc.keys():
                del doc['_id']

            if 'month' in doc.keys():
                del doc['month']

            if 'status' in doc.keys():
                del doc['status']

            if 'timestamp' in doc.keys():
                del doc['timestamp']

            if 'userId' in doc.keys():
                del doc['userId']

            if 'year' in doc.keys():
                del doc['year']

            if 'time' in doc.keys():
                del doc['time']

            if 'info' in doc.keys():
                del doc['info']

            if 'cardNumber' in doc.keys():
                del doc['cardNumber']

            if 'items' in doc.keys():
                del doc['items']

        self.log.debug(docs)

        return {
            'docs': docs,
            'count': n
        }
