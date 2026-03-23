# n8n Workflow Tools — Project Context for AI Assistants

## Project Overview

**Name:** n8n-workflow-tools  
**Type:** Python library / CLI tool  
**Purpose:** Migrate hardcoded absolute paths in n8n workflow JSON files to config-driven, portable format  
**Python:** 3.10+  
**License:** MIT  

## Problem Statement

n8n workflows often hardcode absolute paths (e.g., `C:\Users\john\data.csv` or `/home/john/scripts/run.py`). This breaks workflows when:
- Shared across team members (different home directories)
- Deployed to different environments (dev → prod, local → cloud)
- Moved to different machines or machines

This tool provides automation to extract these paths, generate a config template, and replace them with environment-aware placeholders.

## Architecture

### Core Modules

**src/n8n_workflow_tools/migrator.py**
- `scan_workflows(dir)` — Scan *.json files for hardcoded absolute paths using regex patterns
- `generate_config(scan_results)` — Create config dict mapping detected paths to variable keys
- `apply_config(dir, config)` — Replace hardcoded paths in JSON with `{{KEY}}` placeholders
- `_path_to_key(path)` — Convert path string to valid config identifier (e.g., `/home/justice/scripts/run.py` → `run_py`)

**src/n8n_workflow_tools/cli.py**
- Entry point for command-line usage
- Three subcommands: `scan`, `generate-config`, `apply`
- Handles argparse, JSON I/O, user-facing output formatting

**src/n8n_workflow_tools/__init__.py**
- Version string: `0.1.0`

### Configuration Structure

Config files are JSON:
```json
{
  "paths": {
    "key1": "/original/hardcoded/path",
    "key2": "C:\\Another\\Path"
  }
}
```

When applying, each key becomes a placeholder: `{{KEY1}}`, `{{KEY2}}` (uppercase).

### Path Detection

Regex patterns in `migrator.py`:
- Windows: `[A-Z]:\\\[^\"\'\\\n]+` (matches `C:\...`, `D:\...` etc.)
- Unix: `/(?:home|Users|mnt|opt|var|tmp)/[^\s\"\']+` (matches `/home/...`, `/opt/...` etc.)

Explicitly ignores URLs and localhost references.

## File Structure

```
D:\n8n-workflow-tools/
├── pyproject.toml              # Project metadata, build config
├── LICENSE                     # MIT License
├── README.md                   # User documentation
├── CLAUDE.md                   # This file
├── src/n8n_workflow_tools/
│   ├── __init__.py             # Version string
│   ├── cli.py                  # CLI entry point (n8n-migrate command)
│   └── migrator.py             # Core logic: scan, generate, apply
├── tests/
│   ├── __init__.py
│   └── test_migrator.py        # Pytest tests for migrator functions
├── .github/workflows/
│   ├── release.yml             # PyPI release automation
│   └── ci.yml                  # (Missing) Tests on push/PR
└── skills/                     # Anthropic skills directory (metadata)
```

## Key Implementation Details

### Scan Command
- Recursively finds all `*.json` files in target directory
- Runs regex patterns to detect absolute paths
- Deduplicates paths (same path in multiple files tracked once)
- Returns structured dict with counts and position metadata

### Generate-Config Command
- Takes scan results and creates template config
- Extracts "meaningful" path segments as keys (e.g., last directory name)
- Sanitizes key names (lowercase, alphanumeric + underscore only)
- User must review and edit before applying

### Apply Command
- Loads config JSON
- Builds replacement map: original_path → `{{UPPERCASE_KEY}}`
- Iterates workflow files and performs string replacements
- Preserves JSON structure (no re-serialization, just string substitution)
- Writes only modified files

### Path-to-Key Conversion
- Splits path by `/` or `\`
- Filters out drive letters and empty segments
- Takes last segment as basis
- Replaces `.` and `-` with `_`, removes special chars
- Result: valid Python identifier suitable for config key

## Testing

**Test file:** `tests/test_migrator.py`

Uses pytest fixtures for temporary workflow directories.

**Covered scenarios:**
- Detection of Windows paths
- Detection of Unix paths
- Ignoring non-path patterns (URLs, localhost)
- Empty directory handling
- Config generation from scan results
- Path-to-key conversion for various input formats
- Apply config with replacement verification
- Non-path content preservation

No external dependencies for testing (uses only pytest and stdlib).

## CLI Interface

**Command structure:**
```
n8n-migrate <command> [args]
```

**Commands:**
- `scan <dir> [--json]` — Find paths, optionally JSON output
- `generate-config <dir> [-o FILE]` — Create config template
- `apply <dir> --config FILE` — Replace paths with placeholders

**Entry point:** Defined in `pyproject.toml` as `n8n-migrate = "n8n_workflow_tools.cli:main"`

## Development Workflow

### Adding Features
1. Implement in `migrator.py` (core logic)
2. Expose via `cli.py` if user-facing
3. Add tests in `test_migrator.py`
4. Update README.md with usage examples

### Testing
```bash
pytest tests/ -v           # Run all tests
pytest tests/ -k scan      # Run tests matching "scan"
pytest tests/ -v --tb=short
```

### Manual CLI Testing
```bash
python -m n8n_workflow_tools.cli scan ./test-workflows
```

### Version Bumping
- Update version in `pyproject.toml` and `src/n8n_workflow_tools/__init__.py`
- Tag release: `git tag v0.2.0`
- Push tag to trigger GitHub Actions release workflow

## Dependencies

### Runtime
- None (only stdlib: json, os, re, pathlib, argparse, sys)

### Development
- pytest (for testing)
- hatchling (build backend, declared in pyproject.toml)

### Build/Distribution
- build (CLI tool to build wheels/sdist)
- twine (upload to PyPI)

## Known Limitations & TODOs

- Path patterns are regex-based; obfuscated paths won't be detected
- No support for encoded paths (Base64, hex, etc.)
- Relative paths intentionally skipped (they're portable)
- No path validation (checks if path exists)
- Config keys are auto-generated; conflicts resolved by truncation/numbering (could be improved)
- No built-in diff preview before apply
- Does not integrate with n8n directly (workflows must resolve variables at runtime)

## Future Enhancements

- [ ] Dry-run mode showing proposed changes
- [ ] Interactive mode to confirm/rename paths during apply
- [ ] Support for config inheritance/environment overlays
- [ ] Direct n8n API integration to read/write workflows
- [ ] Path validation against filesystem
- [ ] YAML/TOML config format support
- [ ] Detailed changelog in --verbose mode

## Integration with n8n

This tool prepares workflows but does NOT integrate with n8n directly. After applying config:

1. User manually uploads modified workflow JSON to n8n
2. n8n must be configured to resolve `{{KEY}}` placeholders:
   - Environment variables: `{{process.env.DATA_DIR}}`
   - n8n expressions: custom functions in workflow
   - Centralized config service: n8n webhooks to fetch values

This flexibility allows deployment in any environment without tool modification.

## Contact & Support

Author: Justice  
License: MIT  
Repository: (GitHub URL to be added)

For issues, feature requests, or contributions, please open an issue or PR.
