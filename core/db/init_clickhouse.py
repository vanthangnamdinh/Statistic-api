"""
Script to initialize ClickHouse database and tables
"""
import asyncio
from core.db.clickhouse_session import clickhouse_engine
from core.db.clickhouse_models import Base,engines
from core.config import config
from sqlalchemy import text


async def create_clickhouse_tables():
    """Create ClickHouse tables if they don't exist"""
    try:
        # Create all tables defined in models
        async with clickhouse_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print(f"✅ ClickHouse tables created successfully in database: {config.CLICK_HOUSE_DB}")
        
    except Exception as e:
        print(f"❌ Error creating ClickHouse tables: {str(e)}")
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


async def check_clickhouse_connection():
    """Check if ClickHouse connection is working"""
    try:
        async with clickhouse_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("✅ ClickHouse connection successful")
            return True
    except Exception as e:
        print(f"❌ ClickHouse connection failed: {str(e)}")
        return False


if __name__ == "__main__":
    print("🔧 Initializing ClickHouse...")
    async def main():
        print("🔧 Initializing ClickHouse...")
        
        # Check connection first
        if await check_clickhouse_connection():
            # Create tables
            await create_clickhouse_tables()
        else:
            print("❌ Cannot proceed without ClickHouse connection")
    
    asyncio.run(main())

   