# Features Demonstrated

This repository demonstrates all key features of the VSCode Spark Executor Git integration.

## 1. Git Repository Cloning ✅

**What it tests:**
- HTTPS URL cloning with PAT authentication
- Branch specification
- Commit SHA specification (optional)

**Configuration:**
```yaml
repository:
  git:
    url: https://github.com/username/spark-test-repo.git
    branch: main
    pat_token: ${GIT_PAT_TOKEN}
```

## 2. Custom Dependencies (requirements.txt) ✅

**What it tests:**
- Docker image building with custom packages
- Package installation during build
- Runtime availability of custom packages

**Files:**
- `requirements.txt` - Specifies cerberus and python-dateutil

**What happens:**
1. Requirements detected during clone
2. Hash calculated: `req_hash = sha256(requirements.txt)`
3. Image built with: `pip install -r requirements.txt`
4. Packages available at runtime

## 3. Module Imports from Repository ✅

**What it tests:**
- PYTHONPATH configuration
- Cross-module imports
- Package structure with `__init__.py`

**Structure:**
```
utils/
├── __init__.py          # Makes utils a package
├── data_cleaner.py      # Utility module 1
└── aggregator.py        # Utility module 2

scripts/
└── analysis.py          # Imports from utils
```

**Import examples:**
```python
# In scripts/analysis.py
from utils.data_cleaner import clean_dataframe
from utils.aggregator import calculate_department_summary
```

## 4. Image Caching ✅

**What it tests:**
- Cache key generation
- ACR image existence checks
- Cache hits on repeated runs

**Cache key format:**
```
vscode-spark-{url_hash}-{commit_sha}-{req_hash}
Example: vscode-spark-a1b2c3d4-9f8e7d6c-req5a4b3
```

**Cache scenarios:**
- **First run**: Build new image (~3-5 min)
- **Second run** (same commit + requirements): Use cached image (~0 sec)
- **Script change only**: Use cached image (~0 sec)
- **Requirements change**: Build new image (~3-5 min)
- **New commit**: Build new image (~3-5 min)

## 5. PySpark Operations ✅

**What it tests:**
- DataFrame creation
- Data transformations
- Aggregations
- Built-in Spark functions

**Operations in analysis.py:**
```python
# Create DataFrame
df = spark.createDataFrame(data, schema)

# Filter and clean
df_cleaned = df.filter(col("name").isNotNull())

# Aggregate
stats = df.groupBy("department").agg(
    count("*"),
    avg("salary"),
    sum("salary")
)
```

## 6. Output Variables ✅

**What it tests:**
- Variable capture from script
- Type validation (integer, dict, etc.)
- Structured results

**Outputs:**
```python
# In script
total_count = 13  # integer

department_stats = {  # dict
    "Engineering": {
        "employee_count": 5,
        "avg_salary": 95400.0,
        ...
    },
    ...
}
```

**Configuration:**
```yaml
outputs:
  - variable: total_count
    data_type: integer
  - variable: department_stats
    data_type: dict
```

## Test Scenarios

### Scenario 1: First Run (Cold Cache)

**Steps:**
1. Clone repo
2. Calculate hashes
3. Build image (includes requirements)
4. Push to ACR
5. Execute script
6. Return results

**Expected time:** 3-7 minutes

**Validates:**
- ✅ Git cloning
- ✅ Requirements installation
- ✅ Image building
- ✅ ACR push

### Scenario 2: Second Run (Warm Cache)

**Steps:**
1. Clone repo
2. Calculate hashes
3. Find cached image
4. Execute script
5. Return results

**Expected time:** 1-2 minutes

**Validates:**
- ✅ Cache hit detection
- ✅ ACR image reuse
- ✅ No unnecessary rebuilds

### Scenario 3: Script Modification

**Steps:**
1. Edit scripts/analysis.py in GitHub
2. Commit changes
3. Run executor

**Expected result:** New commit SHA → New image build

**Validates:**
- ✅ Commit-based caching
- ✅ Script changes trigger rebuild

### Scenario 4: Requirements Modification

**Steps:**
1. Edit requirements.txt
2. Commit changes
3. Run executor

**Expected result:** New requirements hash → New image build

**Validates:**
- ✅ Requirements-based caching
- ✅ Dependency changes trigger rebuild

### Scenario 5: Module Import Test

**Steps:**
1. Run scripts/analysis.py
2. Verify no "ModuleNotFoundError"
3. Check output includes department_stats

**Expected result:** Script successfully imports from utils/

**Validates:**
- ✅ PYTHONPATH configuration
- ✅ Module resolution
- ✅ Package structure

## Validation Checklist

After uploading to GitHub and running tests, verify:

- [ ] Repository clones successfully
- [ ] PAT authentication works
- [ ] requirements.txt packages installed
- [ ] Custom modules importable
- [ ] Image builds successfully
- [ ] Image pushes to ACR
- [ ] Cache key generated correctly
- [ ] Second run uses cached image
- [ ] Script executes without errors
- [ ] Output variables captured correctly
- [ ] Cleanup removes temporary repo

## Error Scenarios to Test

### 1. Invalid PAT Token
**Test:** Use wrong token in .env
**Expected:** Clear error message about authentication

### 2. Missing __init__.py
**Test:** Remove utils/__init__.py, commit, run
**Expected:** ModuleNotFoundError with helpful message

### 3. Invalid requirements.txt
**Test:** Add non-existent package to requirements.txt
**Expected:** Build fails with pip error

### 4. Wrong script_file path
**Test:** Set script_file to non-existent file
**Expected:** Error after cloning, before building

### 5. Branch doesn't exist
**Test:** Set branch to "nonexistent-branch"
**Expected:** Git clone fails with branch not found error

## Success Criteria

All tests passing means:
✅ Git integration fully working
✅ Image building operational
✅ Caching system functional
✅ Module imports supported
✅ Requirements handling correct
✅ Error handling comprehensive
