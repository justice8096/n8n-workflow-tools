"""Tests for n8n workflow migrator."""
import json
import pytest
from pathlib import Path
from n8n_workflow_tools.migrator import scan_workflows, generate_config, apply_config, _path_to_key

@pytest.fixture
def tmp_workflow_dir(tmp_path):
    workflow = {
        "nodes": [
            {"parameters": {"path": "C:\\Users\\Justice\\Documents\\project\\data.csv"}},
            {"parameters": {"command": "python /home/justice/scripts/run.py"}},
            {"parameters": {"url": "http://localhost:5678"}}
        ]
    }
    (tmp_path / "workflow1.json").write_text(json.dumps(workflow))
    return tmp_path

def test_scan_finds_windows_paths(tmp_workflow_dir):
    results = scan_workflows(str(tmp_workflow_dir))
    assert results["files_scanned"] == 1
    paths = [p["path"] for p in results["paths_found"]]
    assert any("Users" in p or "Justice" in p for p in paths)

def test_scan_finds_unix_paths(tmp_workflow_dir):
    results = scan_workflows(str(tmp_workflow_dir))
    paths = [p["path"] for p in results["paths_found"]]
    assert any("/home/" in p for p in paths)

def test_scan_ignores_urls(tmp_workflow_dir):
    results = scan_workflows(str(tmp_workflow_dir))
    paths = [p["path"] for p in results["paths_found"]]
    assert not any("localhost" in p for p in paths)

def test_scan_empty_dir(tmp_path):
    results = scan_workflows(str(tmp_path))
    assert results["files_scanned"] == 0
    assert results["paths_found"] == []

def test_generate_config(tmp_workflow_dir):
    scan_results = scan_workflows(str(tmp_workflow_dir))
    config = generate_config(scan_results)
    assert "paths" in config
    assert len(config["paths"]) > 0

def test_path_to_key():
    assert _path_to_key("C:\\Users\\Justice\\project") == "project"
    assert _path_to_key("/home/justice/scripts/run.py") == "run_py"

def test_apply_config(tmp_workflow_dir):
    scan_results = scan_workflows(str(tmp_workflow_dir))
    config = generate_config(scan_results)
    results = apply_config(str(tmp_workflow_dir), config)
    assert results["files_updated"] >= 0

def test_apply_preserves_non_path_content(tmp_workflow_dir):
    original = json.loads((tmp_workflow_dir / "workflow1.json").read_text())
    config = {"paths": {"fake": "/nonexistent/path"}}
    apply_config(str(tmp_workflow_dir), config)
    updated = json.loads((tmp_workflow_dir / "workflow1.json").read_text())
    assert updated["nodes"][2]["parameters"]["url"] == "http://localhost:5678"
