import json
import logging
import redis
from typing import Annotated

from fastapi import APIRouter, HTTPException, Body
from starlette.responses import JSONResponse
from starlette.requests import Request


from app.config.config import RedisSettings
from app.models.validation.user import UserCreate, UserRead
from app.scripts.register import register_user

register_router = APIRouter(
    prefix='',
    tags=["Register"],
)

redis_client = redis.StrictRedis(host=RedisSettings.REDIS_HOST, port=RedisSettings.REDIS_PORT, db=0)


@register_router.post(path='/register')#, response_model=UserRead)
async def create_new_user(new_user: UserCreate,request: Request):
    result = await register_user(request=request, new_user=new_user)
    return JSONResponse(status_code=201,
                        content=result)



