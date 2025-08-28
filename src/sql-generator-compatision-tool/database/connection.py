import json
from pymongo import MongoClient
from sqlalchemy import create_engine

class DatabaseConnection:
    def __init__(self, db_url):
        self.db_url = db_url
        self.connection = None

    def connect(self):
        self.connection = create_engine(self.db_url).connect()

    def close(self):
        if self.connection:
            self.connection.close()

    @staticmethod
    def connect_to_mongodb(config):
        """
        Establishes a connection to MongoDB using the provided configuration.
        """
        return MongoClient(
            host=config.get("host"),
            port=config.get("port"),
            username=config.get("username"),
            password=config.get("password")
        )

    @staticmethod
    def connect_to_mysql_db(config):
        """
        Establishes a connection to MySQL using the provided configuration.
        """
        mysql_url = f"mysql+pymysql://{config.get('username')}:{config.get('password')}@{config.get('host')}:{config.get('port')}/{config.get('database')}"
        return create_engine(mysql_url).connect()

    @staticmethod
    def connect_to_postgresql(config):
        """
        Establishes a connection to PostgreSQL using the provided configuration.
        """
        pg_url = f"postgresql://{config.get('username')}:{config.get('password')}@{config.get('host')}:{config.get('port')}/{config.get('database')}"
        return create_engine(pg_url).connect()

    @staticmethod
    def create_connections(config):
        """
        Creates connections for all schemas in the config based on dbtype.
        Returns a dictionary of connections keyed by schema name.
        """
        connections = {}
        for schema, details in config.items():
            dbdetails = details.get("dbdetails")
            dbtype = dbdetails.get("dbtype")
            connection = None
            if dbtype == "mongodb":
                connection = DatabaseConnection.connect_to_mongodb(dbdetails)
            elif dbtype == "mysql":
                connection = DatabaseConnection.connect_to_mysql_db(dbdetails)
            elif dbtype == "postgresql":
                connection = DatabaseConnection.connect_to_postgresql(dbdetails)
            # Add more dbtypes as needed
            if connection:
                print(f"{dbtype} connection established for schema: {schema}")
            else:
                print(f"No connection established for schema: {schema}")
            connections[schema] = connection
        return connections