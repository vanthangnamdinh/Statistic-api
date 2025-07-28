from asynch import connect, connection
from asynch.cursors import DictCursor

from core.config import config


class ClickHouse:
    @classmethod
    async def create_db(cls, db_name: str) -> bool:
        """Create clickhouse db on first run

        Args:
            db_name (str): name of db
        Returns:
            bool: result
        """
        conn = await connect(
            host=config.CLICK_HOUSE_HOST,
            port=config.CLICK_HOUSE_PORT,
        )
        async with conn.cursor(cursor=DictCursor) as cursor:
            result = await cursor.execute(query=f"create database if not exists {db_name};")
        await conn.close()

        if result:
            return True
        return False

    @classmethod
    async def create_table(cls, table: str) -> bool:
        """Create clickhouse table with table

        Args:
            table (str): name of table
        Returns:
            bool: result
        """
        conn = await cls.conn()
        query = """
            CREATE TABLE IF NOT EXISTS statistic_log (
                id UUID,
                local_timestamp DateTime,
                time_zone String,
                utc_timestamp DateTime,
                user_id String,
                conversation_id String,
                msg_id String,
                activity_type String,
                detail String,
                _source Text,
                current_url String,
                page_title String,
                page_description String,
                page_keywords Array(String),
                user_agent String,
                extension_version String,
                agent_name String,
                agent_version String,
                string_names Array(String),
                string_values Array(String),
                integer_names Array(String),
                integer_values Array(Integer),
                number_names Array(String),
                number_values Array(Float32),
                bool_names Array(String),
                bool_values Array(Bool),
                date_names Array(String),
                date_values Array(DateTime)
            ) ENGINE = MergeTree()
            ORDER BY id;
            """
        async with conn.cursor(cursor=DictCursor) as cursor:
            result = await cursor.execute(query)
        await conn.close()

        if result:
            return True
        return False

    @classmethod
    async def drop_table(cls, table: str) -> bool:
        """drop clickhouse table

        Args:
            table (str): name of table
        Returns:
            bool: result
        """
        conn = await cls.conn()
        query = """
                DROP TABLE  statistic_log
                """
        async with conn.cursor(cursor=DictCursor) as cursor:
            result = await cursor.execute(query)
        await conn.close()

        if result:
            return True
        return False
    @classmethod
    async def conn(cls, ) -> connection.Connection:
        """ click house connection

        Returns:
            connection.Connection: Connection
        """
        return await connect(
            host=config.CLICK_HOUSE_HOST,
            port=config.CLICK_HOUSE_PORT,
            database=config.CLICK_HOUSE_DB,
        )

    @classmethod
    async def execute_sql(cls, query) -> bool:
        """execute sql

        Args:
            query (_type_): sql query
        Returns:
            bool: result
        """
        conn = await cls.conn()
        async with conn.cursor(cursor=DictCursor) as cursor:
            result = await cursor.execute(query)
        await conn.close()

        if result:
            return True
        return False

    @classmethod
    async def fetchall(cls, query: str) -> list:
        """ get many records

        Args:
            query (str): sql query

        Returns:
            list: record dict
        """
        conn = await cls.conn()
        async with conn.cursor(cursor=DictCursor) as cursor:
            await cursor.execute(query)
            ret = cursor.fetchall()
        await conn.close()
        return ret

    @classmethod
    async def fetchone(cls, query: str) -> dict:
        """ get one record

        Args:
            query (str): sql query

        Returns:
            dict: record
        """
        conn = await cls.conn()
        async with conn.cursor(cursor=DictCursor) as cursor:
            await cursor.execute(query)
            ret = cursor.fetchone()
        await conn.close()
        return ret

    @classmethod
    async def insert_many(cls, table: str, values: list) -> bool:
        """ insert_many records

        Args:
            table (str): table name

            values (list): dicts

        Returns:
            bool: insert result
        """
        insert_fields = ','.join([i for i in values[0].keys()])
        conn = await cls.conn()
        async with conn.cursor(cursor=DictCursor) as cursor:
            result = await cursor.execute(
                f"""INSERT INTO {table} ({insert_fields}) VALUES """, values
            )
        await conn.close()
        if result:
            return True
        return False

    @classmethod
    async def insert_one(cls, table: str, value: dict) -> bool:
        """
        Insert a single record into the specified table.

        Args:
            table (str): The name of the table.
            value (dict): A dictionary representing the record to insert.

        Returns:
            bool: True if the insertion was successful, False otherwise.
        """
        # Prepare field names and placeholders
        insert_fields = ', '.join(value.keys())

        # Prepare the values (retain their types)
        insert_values = list(value.values())

        try:
            # Get a database connection
            conn = await cls.conn()

            # Execute the SQL query with parameterized values
            query = f"INSERT INTO {table} ({insert_fields}) VALUES {tuple(insert_values)}"
            print("query", query)
            async with conn.cursor(cursor=DictCursor) as cursor:
                result = await cursor.execute(query)

            # Close the connection
            await conn.close()

            # Check if the insertion was successful
            if result:
                return True
            return False
        except Exception as e:
            # Log the error for debugging purposes
            print(f"Error inserting record into {table}: {e}")
            return False

    @classmethod
    async def check_connection_to_click_house(cls) -> bool:
        """ check click house is alive

        Returns:
            bool: flag_connected
        """
        try:
            conn = await cls.conn()
            flag_connected = conn.connected
            await conn.close()
            return flag_connected
        except Exception as e:
            print(e, flush=True)
            return False


# Singleton instance of the manager
clickhouse_manager = ClickHouse()
