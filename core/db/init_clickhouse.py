"""
Script to initialize ClickHouse database and tables
"""
import asyncio
from core.db.clickhouse_session import clickhouse_engine
from core.db.clickhouse_models import Base,engines
from core.config import config
from sqlalchemy import text
import logging
from sqlalchemy.orm import Session


def create_clickhouse_tables():
    """Create ClickHouse database and tables if they do not exist"""
    try:
        with clickhouse_engine.begin() as conn:
            print(f"Checking if ClickHouse database '{config.CLICK_HOUSE_DB}' exists...")
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {config.CLICK_HOUSE_DB}"))
            Base.metadata.create_all(bind=conn)  # Nếu cần ORM
        print(f"✅ ClickHouse database initialized successfully in database: {config.CLICK_HOUSE_DB}")
    except Exception as e:
        print(f"❌ Error initializing ClickHouse database and tables: {str(e)}")
        raise


async def drop_clickhouse_tables():
    """Drop all ClickHouse tables (use with caution!)"""
    try:
        async with clickhouse_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        
        print(f"✅ ClickHouse tables dropped successfully from database: {config.CLICK_HOUSE_DB}")
        
    except Exception as e:
        print(f"❌ Error dropping ClickHouse tables: {str(e)}")
        raise


def check_clickhouse_connection():
    """Check if ClickHouse connection is successful"""
    try:
        with clickhouse_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result.scalar() == 1:
                print("✅ ClickHouse connection successful")
                return True
            else:
                print("❌ ClickHouse connection failed")
                return False
    except Exception as e:
        print(f"❌ Error connecting to ClickHouse: {str(e)}")
        return False


if __name__ == "__main__":
    print("🔧 Initializing ClickHouse...")

    if check_clickhouse_connection():
        create_clickhouse_tables()
    else:
        print("❌ Cannot proceed without ClickHouse connection")

   