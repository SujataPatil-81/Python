def format_data(data):
    formatted_data = []
    for row in data:
        formatted_row = {key: str(value) for key, value in row.items()}
        formatted_data.append(formatted_row)
    return formatted_data