"""CLI for n8n workflow tools."""
import argparse
import json
import sys
from .migrator import scan_workflows, generate_config, apply_config

def main():
    parser = argparse.ArgumentParser(description="n8n Workflow Path Migrator")
    sub = parser.add_subparsers(dest="command")
    
    scan_cmd = sub.add_parser("scan", help="Scan workflows for hardcoded paths")
    scan_cmd.add_argument("dir", help="Directory containing workflow JSON files")
    scan_cmd.add_argument("--json", action="store_true", help="Output as JSON")
    
    gen_cmd = sub.add_parser("generate-config", help="Generate config template")
    gen_cmd.add_argument("dir", help="Directory containing workflow JSON files")
    gen_cmd.add_argument("--output", "-o", default="config.json", help="Output config file")
    
    apply_cmd = sub.add_parser("apply", help="Apply config to workflows")
    apply_cmd.add_argument("dir", help="Directory containing workflow JSON files")
    apply_cmd.add_argument("--config", "-c", required=True, help="Config JSON file")
    
    args = parser.parse_args()
    
    if args.command == "scan":
        results = scan_workflows(args.dir)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Scanned {results['files_scanned']} files")
            print(f"Found {len(results['paths_found'])} hardcoded paths in {len(results['files_with_paths'])} files")
            for entry in results["paths_found"]:
                print(f"  {entry['file']}: {entry['path']}")
    
    elif args.command == "generate-config":
        scan_results = scan_workflows(args.dir)
        config = generate_config(scan_results)
        with open(args.output, "w") as f:
            json.dump(config, f, indent=2)
        print(f"Config written to {args.output} with {len(config['paths'])} path entries")
    
    elif args.command == "apply":
        with open(args.config) as f:
            config = json.load(f)
        results = apply_config(args.dir, config)
        print(f"Updated {results['files_updated']} files with {results['replacements']} replacements")
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
