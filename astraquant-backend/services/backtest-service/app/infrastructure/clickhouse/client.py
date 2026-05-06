from app.config import settings

class ClickHouseClientFactory:
    def create(self):
        import clickhouse_connect
        return clickhouse_connect.get_client(host=settings.clickhouse_host, port=settings.clickhouse_port, username=settings.clickhouse_username, password=settings.clickhouse_password, database=settings.clickhouse_database)
