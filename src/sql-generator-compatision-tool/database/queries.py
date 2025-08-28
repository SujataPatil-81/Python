
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




def fetch_data(connection, dbtype, querydetails):
    """
    Fetches data from the database based on dbtype and querydetails.
    """
    if dbtype == "mysql":
        # Build SQL query
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

    elif dbtype == "mongodb":
        tablename = querydetails.get("tablename")
        fields = querydetails.get("fields", [])
        where_conditions = querydetails.get("where", {})
        database_name = querydetails.get("database")  # Add this to your config/querydetails if not present
        db = connection[database_name] if database_name else connection.get_default_database()
        collection = db[tablename]
        projection = {field: 1 for field in fields} if fields else None
        cursor = collection.find(where_conditions, projection)
        return list(cursor)

    # Add more dbtypes as needed
    else:
        raise ValueError(f"Unsupported dbtype: {dbtype}")
    from .connection import DatabaseConnection

    db = DatabaseConnection()
    connection = db.connect()
    data = []

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
    finally:
        db.close()

    return data