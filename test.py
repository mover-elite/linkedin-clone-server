import asyncio
import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.test
collection = database.test


async def insert():
    res = await collection.insert_one({"id": 2})
    print(res)


async def read():
    # print(dir(collection))
    collection.find():
        print(do)
    print(dir(collection.find()))
    # print(res)
    # res = await collection


# asyncio.run(read())
