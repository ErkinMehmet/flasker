import re

def sanitize_sql_query(sql_query):
    sql_query = sql_query.strip().lower()
    if not sql_query.startswith("select"):
        raise ValueError("Only SELECT statements are allowed.")
    dangerous_keywords = ["insert", "update", "delete", "drop", "alter", "create"]
    for keyword in dangerous_keywords:
        if re.search(rf'\b{keyword}\b', sql_query):
            raise ValueError(f"Detected a dangerous SQL keyword: {keyword}")

    return sql_query
def convert_to_list(input_string):
    return input_string.split(',')