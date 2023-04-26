import json
from fastapi import APIRouter, Depends, Body
from app.dependencies import get_current_user

from app.schemas.post import PostIn, UserPosts
from app.schemas.comment import CommentIn
from app.schemas.user import User as UserSchema
from app.crud.post import (
    create_post,
    get_all_posts,
    like_post,
    add_comment,
    get_post_info as get_post_info_func,
)
from app.schemas.common import PyObjectId
from app.core.feed import redisFeed


router = APIRouter(prefix="/post")


@router.post("/new", tags=["POSTS"])
async def new_post(
    new_post: PostIn, current_user: UserSchema = Depends(get_current_user)
):
    res = await create_post(new_post, current_user.id)  # type: ignore
    return {"post": res}


@router.get("/posts", tags=["POSTS"])
async def get_posts(current_user: UserSchema = Depends(get_current_user)):
    posts = await get_all_posts()
    return posts


@router.get("/like/{post_id}", tags=["POSTS"])
async def like_post_endpoint(
    post_id: PyObjectId, current_user: UserSchema = Depends(get_current_user)
):
    await like_post(post_id, current_user.id)  # type: ignore


@router.post("/comment", tags=["COMMENT"])
async def common_on_post(
    comment: CommentIn = Body(...),
    current_user: UserSchema = Depends(get_current_user),
):
    new_comment = await add_comment(comment, current_user.id)  # type: ignore

    print(new_comment)
    notification = {
        "entity": "comment",
        "data": {
            "content": new_comment["content"],
            "post_id": str(new_comment["post_id"]),
            "user_id": str(new_comment["user_id"]),
            "user_name": current_user.name,
            "user_username": current_user.username,
            "_id": str(new_comment["_id"]),
        },
    }
    await redisFeed.publish(str(comment.post_id), notification)


@router.get("/{post_id}", tags=["POSTS"])
async def get_post_info(
    post_id: PyObjectId, current_user: UserSchema = Depends(get_current_user)
):
    result = await get_post_info_func(post_id)
    # print(post_id)
    return result
