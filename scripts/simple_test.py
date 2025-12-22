"""Simple test script without custom imports.

This is a simpler script that doesn't require custom utils,
useful for initial testing.
"""

print("=" * 60)
print("SIMPLE EMPLOYEE ANALYSIS")
print("=" * 60)
print()

# Create simple employee data
print("Creating employee data...")
data = [
    ("Alice", "Engineering", 95000),
    ("Bob", "Engineering", 87000),
    ("Carol", "Sales", 75000),
    ("David", "Sales", 68000),
    ("Eve", "Marketing", 72000),
]

df = spark.createDataFrame(data, ["name", "department", "salary"])
print(f"Created DataFrame with {df.count()} rows")
print()

# Show data
print("Employee Data:")
df.show()

# Calculate statistics
print("Calculating statistics...")
from pyspark.sql.functions import count, avg, sum as spark_sum

stats = df.agg(
    count("*").alias("total"),
    avg("salary").alias("avg_salary"),
    spark_sum("salary").alias("total_salary")
).collect()[0]

total_count = stats["total"]
summary_stats = {
    "avg_salary": round(float(stats["avg_salary"]), 2),
    "total_salary": float(stats["total_salary"])
}

print(f"Total employees: {total_count}")
print(f"Average salary: ${summary_stats['avg_salary']:,.2f}")
print(f"Total payroll: ${summary_stats['total_salary']:,.2f}")
print()
print("✅ Script completed successfully!")
