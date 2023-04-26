import redis.asyncio as redis
import asyncio
import json


class RedisFeed:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await redis.from_url(
            "redis://127.0.0.1:6379", decode_responses=True
        )

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def publish(self, channel, message):
        if self.redis:
            await self.redis.publish(channel, json.dumps(message))


redisFeed = RedisFeed()


async def stream_messages(channel):
    try:
        async with redisFeed.redis.pubsub() as pubsub:
            await pubsub.subscribe(channel)
            async for message in pubsub.listen():
                if message["type"] == "subscribe":
                    continue

                print("New Message: ")
                print(message)
                yield json.dumps(message)
    except Exception as e:
        # print(e)
        return


# from app.database.mongodb import database as db
# from pymongo import CursorType
# import asyncio


# async def watch_collections():
#     # Create tailable cursors on the post and comment collections
#     post_cursor = db.posts.find(cursor_type=CursorType.TAILABLE_AWAIT)
#     comment_cursor = db.comments.find(cursor_type=CursorType.TAILABLE_AWAIT)

#     while True:
#         # Wait for a change event from either collection
#         change = await asyncio.gather(post_cursor.next(), comment_cursor.next())

#         # Process the change event
#         print(change)
