# n8n Workflow Tools

A Python library to migrate hardcoded paths in n8n workflow JSON files to a config-driven, environment-agnostic format.

## Problem

n8n workflows often contain hardcoded absolute paths (e.g., `C:\Users\john\data` or `/home/john/scripts`) in node parameters. This makes workflows **not portable** across machines or environments. The same workflow fails when moved to a different computer or deployed to production.

## Solution

This tool provides three commands to solve path portability:

1. **`scan`** — Find all hardcoded absolute paths in workflows
2. **`generate-config`** — Create a config template mapping paths to variable names
3. **`apply`** — Replace hardcoded paths with config placeholders

Workflows then reference paths via variables (e.g., `{{DATA_DIR}}`) that can be resolved at runtime based on the environment.

## Installation

### Via pip (when published to PyPI)

```bash
pip install n8n-workflow-tools
```

### From source

```bash
git clone https://github.com/yourusername/n8n-workflow-tools.git
cd n8n-workflow-tools
pip install -e .
```

## Quick Start

### 1. Scan for hardcoded paths

```bash
n8n-migrate scan ./workflows
```

Output:
```
Scanned 5 files
Found 12 hardcoded paths in 3 files
  workflow1.json: C:\Users\Justice\Documents\project\data.csv
  workflow2.json: /home/justice/scripts/run.py
  workflow1.json: C:\Users\Justice\Documents\archive\
```

Get machine-readable output with `--json`:

```bash
n8n-migrate scan ./workflows --json
```

### 2. Generate config template

```bash
n8n-migrate generate-config ./workflows -o config.json
```

Creates `config.json`:
```json
{
  "paths": {
    "project": "C:\\Users\\Justice\\Documents\\project\\data.csv",
    "run_py": "/home/justice/scripts/run.py",
    "archive": "C:\\Users\\Justice\\Documents\\archive\\"
  }
}
```

Edit this file to specify actual paths for your environment:

```json
{
  "paths": {
    "project": "/mnt/shared/project/data.csv",
    "run_py": "/opt/scripts/run.py",
    "archive": "/mnt/shared/archive/"
  }
}
```

### 3. Apply config to workflows

```bash
n8n-migrate apply ./workflows --config config.json
```

This modifies workflow JSON files in-place, replacing hardcoded paths with `{{PROJECT}}`, `{{RUN_PY}}`, etc.

After applying, your workflow parameters look like:
```json
{
  "nodes": [
    {
      "parameters": {
        "path": "{{PROJECT}}"
      }
    }
  ]
}
```

At runtime, n8n must be configured to resolve these variables. Use environment variables, a centralized config service, or n8n's built-in variable system.

## Usage Examples

### Scenario: Moving workflows from dev to production

**Dev environment:**

```bash
# Scan existing workflows
n8n-migrate scan ./dev-workflows

# Generate config from discovered paths
n8n-migrate generate-config ./dev-workflows -o dev-config.json

# Review and edit dev-config.json to match local paths
```

**Production deployment:**

```bash
# Use production-specific config
cp dev-config.json prod-config.json
# Edit prod-config.json with production paths

# Apply production config
n8n-migrate apply ./workflows --config prod-config.json
```

### Scenario: Team sharing workflows

Create a `config.template.json`:
```json
{
  "paths": {
    "data_dir": "/path/to/shared/data",
    "scripts_dir": "/path/to/shared/scripts"
  }
}
```

Each team member copies it to `config.json`, updates paths for their machine, and applies:
```bash
cp config.template.json config.json
# Edit config.json
n8n-migrate apply ./workflows --config config.json
```

## Requirements

- Python 3.10+
- No external dependencies

## Development

### Setup

```bash
git clone https://github.com/yourusername/n8n-workflow-tools.git
cd n8n-workflow-tools
pip install -e ".[dev]"
```

### Run tests

```bash
pytest tests/
```

### Run CLI locally

```bash
python -m n8n_workflow_tools.cli scan ./test-workflows
```

## How It Works

### Path Detection

The tool uses regex patterns to detect absolute paths:

- **Windows**: `C:\Users\...`, `D:\...`, etc.
- **Unix/Linux**: `/home/...`, `/opt/...`, `/var/...`, etc.

It skips URLs (http://, localhost) and relative paths.

### Config Key Generation

Hardcoded paths are converted to config keys automatically:

- `C:\Users\Justice\Documents\project\data.csv` → `project`
- `/home/justice/scripts/run.py` → `run_py`

The algorithm takes the last meaningful path segment and sanitizes it to valid identifier characters.

### Safe Replacement

When applying config:
- Paths are matched exactly and replaced with placeholders
- JSON structure is preserved
- Non-path content is untouched
- Files are only written if changes are made

## Limitations

- Detects common path patterns; obscured paths (rot13, hex-encoded, etc.) are not detected
- Relative paths are not modified (by design, as they're often portable)
- Does not validate paths or check if they exist
- URL parameters with paths are not currently handled

## Contributing

Issues and pull requests are welcome. Please include test cases for new features.

## License

MIT License — see LICENSE file for details.
