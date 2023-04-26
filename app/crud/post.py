from app.schemas.post import PostIn, Post, UserPosts
from app.schemas.common import PyObjectId
from app.database.mongodb import database
from app.core.exceptions import NotFound
from app.schemas.like import Like, LikeOut
from app.schemas.comment import CommentIn, Comment, UserComment
from app.core.feed import redisFeed


def get_post_collection():
    return database.posts


def get_like_colection():
    return database.likes


def get_comment_collection():
    return database.comments


async def create_post(post: PostIn, user_id: PyObjectId):
    post_colletion = get_post_collection()
    new_post = Post(**post.__dict__, user_id=user_id)  # type: ignore

    res = await post_colletion.insert_one(new_post.dict(exclude_unset=True))
    result = await post_colletion.find_one({"_id": res.inserted_id})
    post = Post(**result)
    return post


async def get_all_posts():
    post_collection = get_post_collection()

    posts = await post_collection.aggregate(
        [
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user_info",
                }
            },
            {"$unwind": "$user_info"},
            {
                "$project": {
                    "_id": 1,
                    "image_url": 1,
                    "content": 1,
                    "timestamp": 1,
                    "user_id": 1,
                    "user_username": "$user_info.username",
                    "user_name": "$user_info.name",
                    "user_email": "$user_info.email",
                }
            },
        ]
    ).to_list(length=20)
    posts = [UserPosts(**post) for post in posts]

    return posts


async def like_post(post_id: PyObjectId, user_id: PyObjectId):
    post_collection = get_post_collection()
    like_collection = get_like_colection()

    res = await post_collection.find_one({"_id": post_id})
    if not res:
        raise NotFound("Post Not Found")

    like_exist = await like_collection.find_one(
        {"entity_id": post_id, "user_id": user_id}
    )
    if like_exist:
        res = await like_collection.delete_one(
            {"entity_id": post_id, "user_id": user_id}
        )
        await redisFeed.publish(
            str(post_id),
            {
                "entity": "like",
                "action": "delete",
                "user_id": str(user_id),
            },
        )
        return

    like = Like(entity_id=post_id, user_id=user_id)  # type: ignore
    res = await like_collection.insert_one(like.dict(exclude_unset=True))
    created = await like_collection.find_one({"_id": res.inserted_id})
    await redisFeed.publish(
        str(post_id),
        {
            "entity": "like",
            "action": "add",
            "user_id": str(user_id),
        },
    )

    return created


async def add_comment(commentIn: CommentIn, user_id: PyObjectId):
    comment_collection = get_comment_collection()
    post_collection = get_post_collection()
    post = await post_collection.find_one({"_id": commentIn.post_id})
    if not post:
        raise NotFound("Invalid POST ID")

    comment = Comment(**commentIn.dict(), user_id=user_id)

    res = await comment_collection.insert_one(comment.dict(exclude_unset=True))
    saved_comment = await comment_collection.find_one({"_id": res.inserted_id})

    return saved_comment


async def get_post_info(post_id: PyObjectId):
    comment_collection = get_comment_collection()
    like_collection = get_like_colection()
    comments = await comment_collection.aggregate(
        [
            {"$match": {"post_id": post_id}},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user_info",
                }
            },
            {"$unwind": "$user_info"},
            {
                "$project": {
                    "_id": 1,
                    "post_id": 1,
                    "content": 1,
                    "user_id": 1,
                    "user_username": "$user_info.username",
                    "user_name": "$user_info.name",
                }
            },
        ]
    ).to_list(length=None)

    likes_query = like_collection.find({"entity_id": post_id})
    likes = [LikeOut(**like) async for like in likes_query]
    comments = [UserComment(**comment) for comment in comments]

    return {"likes": likes, "comments": comments}
