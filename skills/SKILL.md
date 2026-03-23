---
name: n8n-workflow-tools
description: Migrate hardcoded paths in n8n workflows to config-driven portable format
version: 0.1.0
---

# n8n Workflow Tools Skill

Use this skill when the user needs to make n8n workflows portable across machines or environments by externalizing hardcoded paths into a config file.

## When to use
- User is sharing n8n workflows with a team and paths break on different machines
- User mentions hardcoded paths in n8n workflows
- User is setting up n8n workflows on a new machine after cloning a project

## How to use

1. Scan workflows for hardcoded paths:
   ```bash
   python -m n8n_workflow_tools.migrator --scan <workflow-dir>
   ```
2. Generate a config.json template:
   ```bash
   python -m n8n_workflow_tools.migrator --generate-config <workflow-dir>
   ```
3. Apply config to workflows:
   ```bash
   python -m n8n_workflow_tools.migrator --apply <workflow-dir> --config config.json
   ```

## Key behaviors
- Finds all hardcoded absolute paths in workflow JSONs
- Generates a config.json with machine-specific values
- Replaces hardcoded paths with config references
- Run once after cloning or moving a project to a new machine
