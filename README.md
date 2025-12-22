# Spark Test Repository

Sample repository for testing VSCode Spark Executor with git integration and module imports.

## Structure

```
spark-test-repo/
├── README.md
├── requirements.txt          # Custom dependencies
├── utils/                    # Utility modules
│   ├── __init__.py
│   ├── data_cleaner.py      # Data cleaning utilities
│   └── aggregator.py        # Data aggregation utilities
└── scripts/
    └── analysis.py          # Main script that imports from utils
```

## Features

- **Module Imports**: Demonstrates importing custom modules from the repository
- **Custom Dependencies**: Uses requirements.txt for additional packages
- **PySpark Operations**: Real Spark operations with DataFrames
- **Utility Functions**: Reusable data cleaning and aggregation functions

## Usage with VSCode Spark Executor

1. Clone this repository or use git URL in config:
   ```yaml
   repository:
     git:
       url: https://github.com/yourusername/spark-test-repo.git
       branch: main
       pat_token: ${GIT_PAT_TOKEN}
     script_file: scripts/analysis.py
   ```

2. Run with:
   ```bash
   poetry run python -m vscode_tools.spark_executor config.yaml
   ```

## Expected Output

The script will:
1. Create sample employee data
2. Clean data using `utils.data_cleaner`
3. Aggregate by department using `utils.aggregator`
4. Return total count and aggregated statistics
