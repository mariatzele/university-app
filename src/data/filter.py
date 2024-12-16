"""
filter.py
A module to build complex SQL WHERE and HAVING clauses with various
operators and aggregation conditions.
"""
from typing import List, Tuple, Any
from .operators import Operators

class Filter:
    """
    A class to build complex SQL WHERE and HAVING clauses with various
    operators and aggregation conditions.
    """

    def __init__(self):
        self.conditions: List[Tuple[str, Operators, Any]] = []
        self.aggregate_conditions: List[Tuple[str, str, Operators, Any]] = []

    def add_condition(self, column: str, operator: Operators, value):
        """
        Add a condition to the filter (for WHERE clause).

        :param column: The column name.
        :param operator: An instance of the Operators enum.
        :param value: The value to compare or a list of values for IN and NOT_IN.
        """
        if not isinstance(operator, Operators):
            raise ValueError(f"Unsupported operator: {operator}")
        self.conditions.append((column, operator, value))

    def add_aggregate_condition(
        self, column: str, aggregate_operator: str, condition_operator:
            Operators, value):
        """
        Add an aggregate condition (for HAVING clause).

        :param column: The column name to aggregate.
        :param aggregate_operator: The aggregate function (e.g., "AVG", "COUNT").
        :param condition_operator: The operator to use for the condition (e.g., ">", "<", "=").
        :param value: The value to compare the aggregate result against.
        """
        if aggregate_operator not in ["AVG", "COUNT", "SUM", "MIN", "MAX"]:
            raise ValueError(f"Unsupported aggregate operator: {aggregate_operator}")
        self.aggregate_conditions.append(
            (column, aggregate_operator, condition_operator, value)
        )

    def compile(self):
        """
        Compile the filter into a SQL WHERE clause, HAVING clause, a list of
        parameters, and aggregates.

        :return: Tuple (where_clause, having_clause, params, aggregates).
        """
        where_clauses = []
        having_clauses = []
        params = []

        # Compile normal WHERE conditions
        for column, operator, value in self.conditions:
            if operator.requires_list():
                # Handle list-based operators (IN, NOT IN)
                placeholders = ", ".join(["%s"] * len(value))
                where_clauses.append(f"{column} {operator.value} "
                                     f"({placeholders})")
                params.extend(value)
            elif value is None:
                # Handle NULL values
                if operator == Operators.EQ:
                    where_clauses.append(f"{column} IS NULL")
                elif operator == Operators.NE:
                    where_clauses.append(f"{column} IS NOT NULL")
                else:
                    raise ValueError(f"Unsupported operator for NULL value:"
                                     f" {operator}")
            else:
                # Handle standard operators
                where_clauses.append(f"{column} {operator.value} %s")
                params.append(value)

        # Compile aggregate HAVING conditions
        for (
            column,
            aggregate_operator,
            condition_operator,
            value,
        ) in self.aggregate_conditions:
            having_clauses.append(
                f"HAVING {aggregate_operator}({column})"
                f" {condition_operator.value} %s"
            )
            params.append(value)

        where_clause = " AND ".join(where_clauses)
        having_clause = " AND ".join(having_clauses)
        return where_clause, having_clause, params
