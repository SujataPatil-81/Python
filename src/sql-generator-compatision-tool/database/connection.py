import json
from pymongo import MongoClient
from sqlalchemy import create_engine
import urllib.parse

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
        
        """host=urllib.parse.quote_plus(config.get("host"))
        port=urllib.parse.quote_plus(config.get("port"))"""
        host=config.get("host")
        port=config.get("port")
        username = urllib.parse.quote_plus(config.get("username"))
        password = urllib.parse.quote_plus(config.get("password"))
        database = urllib.parse.quote_plus(config.get("database"))


        # Construct the connection URI
        connection_uri = f"mongodb://{username}:{password}@{host}:{port}/{database}"

        # Create a MongoClient instance
        client = MongoClient(connection_uri)

        # Access the specified database
        db = client[database]
        db.command("ping")
        print(f"Successfully connected to MongoDB database: {database}")
        collection = db['ALERTS']
        first_document = collection.find_one()
        #print("First document:", first_document)

        query = {"alert_date": "19/08/2025"}
        alert_document = collection.find_one(query)
        #print("Alerts of date 19th august are:", alert_document)
        #return db
        return client
        

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
                print(f"MongoDB connection established for connection: {connection}")
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