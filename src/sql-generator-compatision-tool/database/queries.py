
import json

def generate_sql_query(querydetails):
    """
    Generates an SQL query based on the querydetails object.
    """
    tablename = querydetails.get("tablename")
    fields = ", ".join(querydetails.get("fields", ["*"]))
    where_conditions = querydetails.get("where", {})
    orderby = querydetails.get("orderby", [])
    joindetails = querydetails.get("joindetails", None)

    # Start building the query
    query = f"SELECT {fields} FROM {tablename}"

    # Add JOIN details if present
    if joindetails:
        join_type = joindetails.get("join_type", "INNER")
        join_table = joindetails.get("table")
        join_on = joindetails.get("on")
        query += f" {join_type} JOIN {join_table} ON {join_on}"

    # Add WHERE conditions if present
    if where_conditions:
        where_clauses = " AND ".join([f"{key} = {json.dumps(value)}" for key, value in where_conditions.items()])
        query += f" WHERE {where_clauses}"

    # Add ORDER BY clause if present
    if orderby:
        query += f" ORDER BY {orderby[0]} {orderby[1]}"

    return query



##sql_query = generate_sql_query(querydetails_schema2)
#print(sql_query)





def fetch_sql_data(connection, dbtype, querydetails):
    """
    Fetches data from SQL databases (MySQL, PostgreSQL, etc.) based on querydetails.
    """
    tablename = querydetails.get("tablename")
    fields = ", ".join(querydetails.get("fields", ["*"]))
    where_conditions = querydetails.get("where", {})
    orderby = querydetails.get("orderby", [])
    joindetails = querydetails.get("joindetails", None)

    query = f"SELECT {fields} FROM {tablename}"
    if joindetails:
        join_type = joindetails.get("join_type", "INNER")
        join_table = joindetails.get("table")
        join_on = joindetails.get("on")
        query += f" {join_type} JOIN {join_table} ON {join_on.get('left_field')} = {join_on.get('right_field')}"
    if where_conditions:
        where_clauses = " AND ".join([f"{key} = '{value}'" for key, value in where_conditions.items()])
        query += f" WHERE {where_clauses}"
    if orderby:
        query += f" ORDER BY {orderby[0]} {orderby[1]}"
    result = connection.execute(query)
    return result.fetchall()

def fetch_mongo_data(client, database, querydetails):
    """
    Fetches data from MongoDB based on querydetails.
    """
    db = client[database]
    db.command("ping")
    print(f"Successfully connected to MongoDB database: {database}")
    collection_name = querydetails.get("collection", "ALERTS")
    collection = db[collection_name]
    query = querydetails.get("query", {"alert_date": "19/08/2025"})
    first_document = collection.find_one()
    documents = list(collection.find(query))
    print("first_document fetched are:", first_document)
    return documents