"""Data aggregation utilities for PySpark DataFrames.

This module provides functions to aggregate and summarize data in Spark DataFrames.
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, sum as spark_sum, avg, count, min as spark_min, max as spark_max


def aggregate_by_column(df: DataFrame, group_by: str, agg_column: str) -> DataFrame:
    """Aggregate DataFrame by grouping column.

    Args:
        df: Input DataFrame
        group_by: Column to group by
        agg_column: Column to aggregate (sum)

    Returns:
        Aggregated DataFrame with sum

    Example:
        >>> dept_totals = aggregate_by_column(df, "department", "salary")
    """
    return df.groupBy(group_by).agg(
        spark_sum(agg_column).alias(f"total_{agg_column}")
    )


def calculate_statistics(df: DataFrame, numeric_column: str) -> dict:
    """Calculate statistics for a numeric column.

    Args:
        df: Input DataFrame
        numeric_column: Column to calculate statistics for

    Returns:
        Dictionary with statistics (count, avg, min, max, sum)

    Example:
        >>> stats = calculate_statistics(df, "salary")
        >>> print(stats["avg"])
    """
    result = df.agg(
        count(numeric_column).alias("count"),
        avg(numeric_column).alias("avg"),
        spark_min(numeric_column).alias("min"),
        spark_max(numeric_column).alias("max"),
        spark_sum(numeric_column).alias("sum")
    ).collect()[0]

    return {
        "count": result["count"],
        "avg": float(result["avg"]) if result["avg"] else 0.0,
        "min": float(result["min"]) if result["min"] else 0.0,
        "max": float(result["max"]) if result["max"] else 0.0,
        "sum": float(result["sum"]) if result["sum"] else 0.0,
    }


def group_and_sum(df: DataFrame, group_cols: list, sum_cols: list) -> DataFrame:
    """Group DataFrame and sum multiple columns.

    Args:
        df: Input DataFrame
        group_cols: Columns to group by (list)
        sum_cols: Columns to sum (list)

    Returns:
        Grouped and aggregated DataFrame

    Example:
        >>> result = group_and_sum(
        ...     df,
        ...     group_cols=["department", "location"],
        ...     sum_cols=["salary", "bonus"]
        ... )
    """
    # Build aggregation expressions
    agg_exprs = [spark_sum(col).alias(f"total_{col}") for col in sum_cols]

    return df.groupBy(*group_cols).agg(*agg_exprs)


def calculate_department_summary(df: DataFrame) -> dict:
    """Calculate summary statistics by department.

    Args:
        df: Input DataFrame with 'department' and 'salary' columns

    Returns:
        Dictionary with department summaries

    Example:
        >>> summary = calculate_department_summary(employee_df)
        >>> print(summary["Engineering"]["avg_salary"])
    """
    # Group by department and calculate stats
    dept_stats = df.groupBy("department").agg(
        count("*").alias("employee_count"),
        avg("salary").alias("avg_salary"),
        spark_sum("salary").alias("total_payroll"),
        spark_min("salary").alias("min_salary"),
        spark_max("salary").alias("max_salary")
    ).collect()

    # Convert to dictionary
    summary = {}
    for row in dept_stats:
        dept = row["department"]
        summary[dept] = {
            "employee_count": row["employee_count"],
            "avg_salary": round(float(row["avg_salary"]), 2),
            "total_payroll": round(float(row["total_payroll"]), 2),
            "min_salary": float(row["min_salary"]),
            "max_salary": float(row["max_salary"])
        }

    return summary
