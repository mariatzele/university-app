"""
util.py
A module that converts a filter dictionary into a WHERE clause for SQL queries.
"""
def compile_filter(filter: dict):
    """
    Convert a filter dictionary into a WHERE clause for SQL queries.

    :param filter: Dictionary of filters, where the key is the column name
                   and the value is the value or list of values for that column.
    :return: Tuple with the WHERE clause string and the list of parameters.
    """
    where_clauses = []
    params = []

    for key, value in filter.items():
        if isinstance(value, list):
            # If the value is a list, use IN clause
            placeholders = ", ".join(["%s"] * len(value))
            where_clauses.append(f"{key} IN ({placeholders})")
            params.extend(value)
        else:
            # If the value is a single value, use = clause
            where_clauses.append(f"{key} = %s")
            params.append(value)

    where_clause = " AND ".join(where_clauses)  # Join the clauses with AND
    return where_clause, params
