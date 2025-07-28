import os

import click
import uvicorn

from core.config import config
from core.db.init_clickhouse import create_clickhouse_tables, check_clickhouse_connection

import asyncio


@click.command()
@click.option(
    "--env",
    type=click.Choice(["local", "dev", "prod"], case_sensitive=False),
    default="local",
)
@click.option(
    "--debug",
    type=click.BOOL,
    is_flag=True,
    default=False,
)
def main(env: str, debug: bool):
    os.environ["ENV"] = env
    os.environ["DEBUG"] = str(debug)
    uvicorn.run(
        app="app.server:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True if config.ENV != "production" else False,
        workers=1,
    )


if __name__ == "__main__":
    async def init_clickhouse():
        print("🔧 Initializing ClickHouse...")
        
        # Check connection first
        if await check_clickhouse_connection():
            # Create tables
            await create_clickhouse_tables()
        else:
            print("❌ Cannot proceed without ClickHouse connection")

    asyncio.run(init_clickhouse())
    main()
