import os
from database.connection import DatabaseConnection
from database.queries import fetch_data
from csv_generator.generator import generate_csv
from utils.file_utils import read_config

file_path = "config/db_config.json"

def main():
    # Read configuration
    config = read_config(file_path)

    # Create connections for all schemas
    connections = DatabaseConnection.create_connections(config)

    try:
        for schema, details in config.items():
            dbdetails = details.get("dbdetails")
            querydetails = details.get("querydetails")
            dbtype = dbdetails.get("dbtype")
            connection = connections.get(schema)
            if connection:
                print(f"Fetching data for schema: {schema} (dbtype: {dbtype})")
                data = fetch_data(connection, dbtype, querydetails)
                generate_csv(data, filename=f"{schema}_output.csv")
            else:
                print(f"No connection available for schema: {schema}")
                
        print("end of try")

    finally:
        # Close all connections
        for conn in connections.values():
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass

if __name__ == "__main__":
    main()