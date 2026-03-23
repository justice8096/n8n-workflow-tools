"""n8n workflow path migrator — scan, generate config, and apply."""
import json
import os
import re
from pathlib import Path

# Common patterns for absolute paths
PATH_PATTERNS = [
    re.compile(r'[A-Z]:\\\\[^"\'\\n]+', re.IGNORECASE),  # Windows paths
    re.compile(r'/(?:home|Users|mnt|opt|var|tmp)/[^\s"\']+'),  # Unix absolute paths
]

def scan_workflows(workflow_dir: str) -> dict:
    """Scan n8n workflow JSONs for hardcoded absolute paths."""
    results = {"files_scanned": 0, "paths_found": [], "files_with_paths": []}
    workflow_path = Path(workflow_dir)
    
    for json_file in workflow_path.glob("*.json"):
        results["files_scanned"] += 1
        content = json_file.read_text(encoding="utf-8")
        file_paths = []
        
        for pattern in PATH_PATTERNS:
            for match in pattern.finditer(content):
                path_str = match.group().rstrip('",}]')
                if path_str not in [p["path"] for p in file_paths]:
                    file_paths.append({
                        "path": path_str,
                        "file": json_file.name,
                        "position": match.start()
                    })
        
        if file_paths:
            results["paths_found"].extend(file_paths)
            results["files_with_paths"].append(json_file.name)
    
    return results

def generate_config(scan_results: dict) -> dict:
    """Generate a config.json template from scan results."""
    config = {"paths": {}}
    seen = set()
    
    for entry in scan_results["paths_found"]:
        path_str = entry["path"]
        # Create a variable name from the path
        key = _path_to_key(path_str)
        if key not in seen:
            config["paths"][key] = path_str
            seen.add(key)
    
    return config

def _path_to_key(path_str: str) -> str:
    """Convert a path to a config key name."""
    # Take the last meaningful directory/file name
    parts = re.split(r'[/\\]+', path_str.strip('/\\'))
    meaningful = [p for p in parts if p and not re.match(r'^[A-Z]:?$', p, re.I)]
    if meaningful:
        key = meaningful[-1].replace('.', '_').replace('-', '_').lower()
        return re.sub(r'[^a-z0-9_]', '', key)
    return "path_unknown"

def apply_config(workflow_dir: str, config: dict) -> dict:
    """Replace hardcoded paths in workflows with config references."""
    results = {"files_updated": 0, "replacements": 0}
    workflow_path = Path(workflow_dir)
    
    # Build replacement map: original_path -> {{CONFIG_KEY}}
    replacements = {}
    for key, original_path in config.get("paths", {}).items():
        replacements[original_path] = "{{" + key.upper() + "}}"
    
    for json_file in workflow_path.glob("*.json"):
        content = json_file.read_text(encoding="utf-8")
        original = content
        
        for old_path, placeholder in sorted(replacements.items(), key=lambda x: -len(x[0])):
            if old_path in content:
                content = content.replace(old_path, placeholder)
                results["replacements"] += 1
        
        if content != original:
            json_file.write_text(content, encoding="utf-8")
            results["files_updated"] += 1
    
    return results
