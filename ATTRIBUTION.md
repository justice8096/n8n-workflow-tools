# Attribution

> Record of human and AI contributions to this project.

## Project

- **Name:** n8n-workflow-tools
- **Repository:** https://github.com/justice8096/n8n-workflow-tools
- **Started:** 2025 (embedded in TarotCardProject)

---

## Contributors

### Human

| Name | Role | Areas |
|------|------|-------|
| Justice E. Chase | Lead developer | Architecture, design, domain logic, review, integration |

### AI Tools Used

| Tool | Model/Version | Purpose |
|------|---------------|---------|
| Claude | Claude Opus 4.6 | Code generation, documentation, testing, research |
| Claude Code | — | Agentic development, refactoring, extraction |

---

## Contribution Log

### Original Source Code
Extracted from TarotCardProject/update_workflow_paths.py. Justice designed the config-driven path migration approach and the --scan mode concept.

| Date | Tag | Description | AI Tool | Human Review |
|------|-----|-------------|---------|--------------|
| 2025-2026 | `human-only` | Original config-driven path migration architecture, --scan mode design | — | Justice E. Chase |

### Standalone Extraction

| Date | Tag | Description | AI Tool | Human Review |
|------|-----|-------------|---------|--------------|
| 2026-03-21 | `ai-assisted` | Extracted from TarotCardProject into standalone repo, pyproject.toml, CLI wrapper | Claude Code | Architecture decisions, reviewed all code |
| 2026-03-21 | `ai-generated` | Package config, CI/CD workflows (ci.yml), LICENSE | Claude Code | Reviewed and approved |
| 2026-03-21 | `ai-generated` | README documentation, CLAUDE.md | Claude Code | Reviewed, edited |

### Improvements (2026-03-23)

| Date | Tag | Description | AI Tool | Human Review |
|------|-----|-------------|---------|--------------|
| 2026-03-23 | `ai-generated` | Test suite, configuration validation tests | Claude Code | Reviewed and approved |
| 2026-03-23 | `ai-assisted` | Documentation enhancements, migration examples | Claude Code | Reviewed and edited |

---

## Commit Convention

Include `[ai:claude]` tag in commit messages for AI-assisted or AI-generated changes. Example:
```
Extract workflow tools and add tests [ai:claude]
```

---

## Disclosure Summary

| Category | Approximate % |
|----------|---------------|
| Human-only code | 25% |
| AI-assisted code | 30% |
| AI-generated (reviewed) | 45% |
| Documentation | 90% AI-assisted |
| Tests | 95% AI-generated |

---

## Notes

- All AI-generated or AI-assisted code is reviewed by a human contributor before merging.
- AI tools do not have repository access or commit privileges.
- This file is maintained manually and may not capture every interaction.
- Original source code was embedded in TarotCardProject before extraction.

---

## License Considerations

AI-generated content may have different copyright implications depending on jurisdiction. See [LICENSE](./LICENSE) for this project's licensing terms. Contributors are responsible for ensuring AI-assisted work complies with applicable policies.
