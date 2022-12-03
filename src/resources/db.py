from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCursor

import config


async def test_connection(client: AsyncIOMotorClient) -> None:
    await client.admin.command("ping")


async def get_client(mongo_uri: Optional[str] = None) -> AsyncIOMotorClient:
    if mongo_uri is None:
        mongo_uri = config.MONGODB_URI

    client = AsyncIOMotorClient(mongo_uri)
    await test_connection(client)
    return client


async def get_db(client: AsyncIOMotorClient) -> AsyncIOMotorCursor:
    return client[config.MONGODB_DATABASE]
