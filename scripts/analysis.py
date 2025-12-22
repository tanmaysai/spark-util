"""Employee Data Analysis Script.

This script demonstrates:
1. Importing custom utility modules from the repository
2. Using PySpark for data processing
3. Cleaning data with custom utilities
4. Aggregating data by department
5. Returning structured results

Expected outputs:
- total_count: Total number of employees (integer)
- department_stats: Statistics by department (dict)
"""

# Import custom utilities from our repository
from utils.data_cleaner import clean_dataframe, validate_salary
from utils.aggregator import calculate_department_summary, calculate_statistics

print("=" * 60)
print("EMPLOYEE DATA ANALYSIS")
print("=" * 60)
print()

# Step 1: Create sample employee data
print("Step 1: Creating sample employee data...")
employee_data = [
    ("Alice Johnson", "Engineering", 95000),
    ("Bob Smith", "Engineering", 87000),
    ("Carol White", "Sales", 75000),
    ("David Brown", "Sales", 68000),
    ("Eve Davis", "Marketing", 72000),
    ("Frank Wilson", "Engineering", 105000),
    ("Grace Lee", "Marketing", 78000),
    ("Henry Chen", "Sales", 82000),
    ("Iris Taylor", "Engineering", 92000),
    ("Jack Anderson", "Marketing", 85000),
    # Add some data with issues for cleaning
    ("  Lisa Miller  ", "Sales", 71000),  # Extra whitespace
    ("Mike Garcia", "Engineering", 98000),
    ("Nancy Martinez", "Marketing", 74000),
    (None, "Sales", 65000),  # Null name (will be filtered)
    ("Oscar Rodriguez", None, 88000),  # Null department (will be filtered)
]

df = spark.createDataFrame(employee_data, ["name", "department", "salary"])
print(f"  Created DataFrame with {df.count()} rows")
print()

# Step 2: Clean the data using custom utilities
print("Step 2: Cleaning data with custom utilities...")
df_cleaned = clean_dataframe(df)
df_cleaned = validate_salary(df_cleaned, "salary")
print(f"  After cleaning: {df_cleaned.count()} rows")
print()

# Step 3: Show cleaned data sample
print("Step 3: Sample of cleaned data:")
df_cleaned.show(5, truncate=False)
print()

# Step 4: Calculate department statistics using custom aggregator
print("Step 4: Calculating department statistics...")
department_stats = calculate_department_summary(df_cleaned)

print("  Department Summary:")
for dept, stats in department_stats.items():
    print(f"    {dept}:")
    print(f"      Employees: {stats['employee_count']}")
    print(f"      Avg Salary: ${stats['avg_salary']:,.2f}")
    print(f"      Total Payroll: ${stats['total_payroll']:,.2f}")
    print(f"      Salary Range: ${stats['min_salary']:,.0f} - ${stats['max_salary']:,.0f}")
print()

# Step 5: Calculate overall statistics
print("Step 5: Calculating overall statistics...")
overall_stats = calculate_statistics(df_cleaned, "salary")
print(f"  Total Employees: {overall_stats['count']}")
print(f"  Average Salary: ${overall_stats['avg']:,.2f}")
print(f"  Total Payroll: ${overall_stats['sum']:,.2f}")
print()

# Step 6: Calculate total count for output
total_count = df_cleaned.count()

print("=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
print(f"Total employees analyzed: {total_count}")
print(f"Departments: {len(department_stats)}")
print()

# Output variables (MUST match config file)
# These will be captured by SparkScriptExecutor and returned to user
print("Setting output variables...")
print(f"  total_count = {total_count}")
print(f"  department_stats = {department_stats}")
print()
print("✅ Script completed successfully!")
