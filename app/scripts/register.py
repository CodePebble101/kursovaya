import json
import logging

import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.validation.user import UserCreate, User


async def get_register_data_from_mongo(request, username: str):
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client['test_db']
    cursor = mongo_client.users.find({"username": username})
    result_data = None
    for document in await cursor.to_list(length=10):
        document["_id"] = str(document["_id"])
        result_data = document
    return result_data


async def register_user(request, new_user: UserCreate):
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client['test_db']
    cursor = mongo_client.users.insert_one(dict(new_user))
    return dict(new_user)
