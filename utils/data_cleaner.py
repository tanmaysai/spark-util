"""Data cleaning utilities for PySpark DataFrames.

This module provides functions to clean and standardize data in Spark DataFrames.
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, trim, upper, regexp_replace


def clean_dataframe(df: DataFrame) -> DataFrame:
    """Clean DataFrame by removing nulls and standardizing text.

    Args:
        df: Input Spark DataFrame

    Returns:
        Cleaned DataFrame

    Example:
        >>> cleaned_df = clean_dataframe(raw_df)
    """
    # Remove rows with null values in critical columns
    df_cleaned = remove_nulls(df, ["name", "department"])

    # Standardize name formatting
    df_cleaned = standardize_names(df_cleaned, "name")

    return df_cleaned


def remove_nulls(df: DataFrame, columns: list) -> DataFrame:
    """Remove rows with null values in specified columns.

    Args:
        df: Input DataFrame
        columns: List of column names to check for nulls

    Returns:
        DataFrame with nulls removed

    Example:
        >>> df_no_nulls = remove_nulls(df, ["id", "name"])
    """
    for column in columns:
        if column in df.columns:
            df = df.filter(col(column).isNotNull())

    return df


def standardize_names(df: DataFrame, column: str) -> DataFrame:
    """Standardize name formatting in a column.

    - Trims whitespace
    - Converts to title case (first letter capitalized)
    - Removes extra spaces

    Args:
        df: Input DataFrame
        column: Name of column to standardize

    Returns:
        DataFrame with standardized names

    Example:
        >>> df_clean = standardize_names(df, "employee_name")
    """
    if column not in df.columns:
        return df

    # Trim whitespace
    df = df.withColumn(column, trim(col(column)))

    # Remove multiple spaces
    df = df.withColumn(column, regexp_replace(col(column), r"\s+", " "))

    return df


def validate_salary(df: DataFrame, salary_column: str = "salary") -> DataFrame:
    """Validate and clean salary data.

    - Removes negative salaries
    - Filters out unrealistic values (< 0 or > 10M)

    Args:
        df: Input DataFrame
        salary_column: Name of salary column

    Returns:
        DataFrame with validated salaries

    Example:
        >>> df_valid = validate_salary(df, "annual_salary")
    """
    if salary_column not in df.columns:
        return df

    # Remove negative or unrealistic salaries
    df = df.filter(
        (col(salary_column) >= 0) &
        (col(salary_column) <= 10000000)  # Max 10M
    )

    return df
