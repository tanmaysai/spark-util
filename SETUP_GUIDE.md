# Setup Guide - Upload to GitHub

## Step 1: Initialize Git Repository

```bash
cd /Users/tanmay.shrivastava/projects/spark-test-repo

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Sample Spark repository with custom utils"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `spark-test-repo`
3. Description: "Sample Spark repository for testing module imports"
4. Visibility: **Public** (or Private if you prefer)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 3: Push to GitHub

After creating the repo, GitHub will show you commands. Use these:

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/spark-test-repo.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Create Personal Access Token (PAT)

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Token name: `vscode-spark-executor`
4. Expiration: 90 days (or as needed)
5. Scopes: Check `repo` (all sub-scopes)
6. Click "Generate token"
7. **COPY THE TOKEN** - you won't see it again!

## Step 5: Configure .env File

Add the token to your sail-flows `.env` file:

```bash
cd /Users/tanmay.shrivastava/projects/sail-flows

# Add this line to .env
echo "GIT_PAT_TOKEN=ghp_your_token_here" >> .env
```

Replace `ghp_your_token_here` with your actual token.

## Step 6: Create Configuration File

Create a config file in sail-flows vscode_tools directory:

```bash
cd /Users/tanmay.shrivastava/projects/sail-flows/vscode_tools
```

Create `test_git_config.yaml`:

```yaml
environment: dev

repository:
  git:
    url: https://github.com/YOUR_USERNAME/spark-test-repo.git
    branch: main
    pat_token: ${GIT_PAT_TOKEN}
  script_file: scripts/analysis.py

outputs:
  - variable: total_count
    data_type: integer
  - variable: department_stats
    data_type: dict

spark:
  driver_cores: 1
  driver_memory: 512m
  executor_count: 1
  executor_cores: 1
  executor_memory: 512m
```

**Don't forget to replace `YOUR_USERNAME` with your actual GitHub username!**

## Step 7: Test the Setup

### Test 1: Simple script (no custom imports)

```bash
cd /Users/tanmay.shrivastava/projects/sail-flows

# Create simple config
cat > vscode_tools/test_git_simple.yaml << 'EOF'
environment: dev

repository:
  git:
    url: https://github.com/YOUR_USERNAME/spark-test-repo.git
    branch: main
    pat_token: ${GIT_PAT_TOKEN}
  script_file: scripts/simple_test.py

outputs:
  - variable: total_count
    data_type: integer
  - variable: summary_stats
    data_type: dict
EOF

# Run test
poetry run python -m vscode_tools.spark_executor vscode_tools/test_git_simple.yaml
```

### Test 2: Full script with custom imports

```bash
# Run full analysis script
poetry run python -m vscode_tools.spark_executor vscode_tools/test_git_config.yaml
```

## Expected Output

### First Run (Cold Cache):
```
✓ Configuration loaded and validated
  Repository: https://github.com/YOUR_USERNAME/spark-test-repo.git
  Branch: main
  Script: scripts/analysis.py

⏳ Building workflow...

⏳ Cloning git repository...
✓ Repository cloned to: /tmp/vscode-spark-repos/abc-123
  Commit: a1b2c3d4
  Requirements hash: e5f6g7h8
  Cache key: vscode-spark-12345678-a1b2c3d4-e5f6g7h8

⏳ Checking for cached image...
⏳ Building custom image (this may take a few minutes)...
  Step 1/4: FROM crescendoimages.azurecr.io/pyspark-script-runner:base
  Step 2/4: COPY . /opt/spark/work-dir/repo/
  Step 3/4: Installing requirements from requirements.txt...
  Step 4/4: Setting PYTHONPATH...
✓ Image built and pushed in 127.3s

⏳ Building workflow...
✓ Converting to DSL...
✓ Workflow submitted to Temporal (workflow_id: abc-123)
  View in Temporal UI: https://sail-temporal.accelerate.symphonyai.com/namespaces/default/workflows/abc-123

⏳ Waiting for Spark job to complete...

✅ Execution completed successfully! (52 seconds)

Results:
  total_count: 13
  department_stats: {'Engineering': {'employee_count': 5, 'avg_salary': 95400.0, ...}, ...}

✓ Cleaned up temporary repository
```

### Second Run (Warm Cache):
```
✓ Configuration loaded and validated
  Repository: https://github.com/YOUR_USERNAME/spark-test-repo.git
  Branch: main
  Script: scripts/analysis.py

⏳ Building workflow...

⏳ Cloning git repository...
✓ Repository cloned to: /tmp/vscode-spark-repos/xyz-789
  Commit: a1b2c3d4
  Requirements hash: e5f6g7h8
  Cache key: vscode-spark-12345678-a1b2c3d4-e5f6g7h8

⏳ Checking for cached image...
✓ Using cached image: vscode-spark-12345678-a1b2c3d4-e5f6g7h8

⏳ Building workflow...
✓ Converting to DSL...
✓ Workflow submitted to Temporal

⏳ Waiting for Spark job to complete...

✅ Execution completed successfully! (42 seconds)
```

## Troubleshooting

### "Authentication failed"
- Check that PAT token is correctly set in `.env`
- Verify token has `repo` scope
- Test with: `curl -H "Authorization: token ${GIT_PAT_TOKEN}" https://api.github.com/user`

### "Repository not found"
- Verify repository URL is correct
- If repo is private, ensure PAT has access
- Check spelling of username and repo name

### "Docker daemon not running"
- Start Docker Desktop
- Verify: `docker ps`

### "Module not found: utils"
- This means PYTHONPATH wasn't set correctly
- Check that Dockerfile sets PYTHONPATH
- Verify utils/__init__.py exists in repo

## Repository Structure

```
spark-test-repo/
├── README.md                 # Repository overview
├── SETUP_GUIDE.md           # This file
├── requirements.txt         # Custom dependencies
├── .gitignore              # Git ignore patterns
├── config_example.yaml     # Example config
├── utils/                  # Custom utility modules
│   ├── __init__.py        # Package init
│   ├── data_cleaner.py    # Data cleaning utilities
│   └── aggregator.py      # Data aggregation utilities
└── scripts/
    ├── analysis.py        # Main analysis (with imports)
    └── simple_test.py     # Simple test (no imports)
```

## Next Steps

After successful testing:
1. Try modifying the script and re-running (should use cached image)
2. Try modifying requirements.txt (should trigger new build)
3. Try creating a new branch and using that in config
4. Try specifying a commit SHA instead of branch
