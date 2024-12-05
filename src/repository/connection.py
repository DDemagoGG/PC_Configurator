"""Postgresql connector."""
import typing
import urllib.parse
from contextlib import asynccontextmanager

import pydantic
from asyncpg import Connection, Pool, create_pool
from psycopg2.extras import RealDictCursor

__all__ = ["Postgresql"]


class Connector:
    username: str
    password: pydantic.SecretStr
    host: pydantic.PositiveInt
    port: pydantic.PositiveInt
    database_name: str
    pool: Pool = None

    def __init__(
        self, username: str, password: str, host: str, port: int, database_name: str
    ):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name

    @asynccontextmanager
    async def get_connect(self):
        if self.pool is None:
            self.pool = await create_pool(
                user=self.username,
                password=self.password,
                database=self.database_name,
                host=self.host,
                port=self.port,
            )

        async with self.pool.acquire() as conn:
            yield conn
