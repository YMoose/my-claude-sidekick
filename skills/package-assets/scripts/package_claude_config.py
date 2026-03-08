#!/usr/bin/env python3
"""Package Claude configurations into a ZIP file."""

import argparse
import json
import os
import zipfile
from pathlib import Path
from datetime import datetime
import shutil

def get_claude_base_dir():
    """Get the Claude base directory, respecting custom configurations."""
    # Check environment variable first
    env_dir = os.environ.get("CLAUDE_CONFIG_DIR")
    if env_dir:
        return Path(env_dir).expanduser()

    # Check for .claude.json in home directory (custom config path)
    claude_json = Path.home() / ".claude.json"
    if claude_json.exists():
        try:
            config = json.loads(claude_json.read_text())
            if "configDir" in config:
                return Path(config["configDir"]).expanduser()
        except (json.JSONDecodeError, KeyError):
            pass

    # Default to ~/.claude
    return Path.home() / ".claude"

def find_claude_config_dirs():
    """Find all relevant Claude config directories."""
    base = get_claude_base_dir()

    dirs = {
        "skills": [],
        "agents": [],
        "plugins": [],
        "projects": [],
        "scripts": None,
        "settings": base / "settings.json"
    }

    # Find skills directories (user-created, not plugin skills)
    skills_base = base / "skills"
    if skills_base.exists():
        dirs["skills"].append(str(skills_base))

    # Find agents directories (user-created, not plugin agents)
    agents_base = base / "agents"
    if agents_base.exists():
        dirs["agents"].append(str(agents_base))

    # Find plugins (cache and marketplaces)
    plugins_dir = base / "plugins"
    if plugins_dir.exists():
        # Include cache (installed plugins)
        cache_dir = plugins_dir / "cache"
        if cache_dir.exists():
            dirs["plugins"].append(str(cache_dir))
        # Include marketplaces (plugin definitions)
        marketplaces_dir = plugins_dir / "marketplaces"
        if marketplaces_dir.exists():
            dirs["plugins"].append(str(marketplaces_dir))

    # Find project configs
    projects_dir = base / "projects"
    if projects_dir.exists():
        for proj in projects_dir.iterdir():
            if proj.is_dir():
                claude_md = proj / "CLAUDE.md"
                if claude_md.exists():
                    dirs["projects"].append(str(proj))

    # Custom scripts
    scripts_dir = base / "scripts"
    if scripts_dir.exists():
        dirs["scripts"] = str(scripts_dir)

    return dirs

def collect_files(dirs, options):
    """Collect all files to package based on options."""
    files = {}

    if options.get("skills"):
        files["skills"] = []
        for skills_dir in dirs["skills"]:
            skills_path = Path(skills_dir)
            for md_file in skills_path.rglob("*.md"):
                # Skip plugin skills (they're packaged separately)
                if "plugins" in str(md_file):
                    continue
                rel_path = md_file.relative_to(skills_path)
                files["skills"].append({
                    "source": str(md_file),
                    "relative": str(rel_path)
                })

    if options.get("agents"):
        files["agents"] = []
        for agents_dir in dirs["agents"]:
            agents_path = Path(agents_dir)
            for md_file in agents_path.rglob("*.md"):
                # Skip plugin agents
                if "plugins" in str(md_file):
                    continue
                rel_path = md_file.relative_to(agents_path)
                files["agents"].append({
                    "source": str(md_file),
                    "relative": str(rel_path)
                })

    if options.get("plugins"):
        files["plugins"] = []
        for plugins_dir in dirs["plugins"]:
            plugins_path = Path(plugins_dir)
            for item in plugins_path.rglob("*"):
                if item.is_file():
                    rel_path = item.relative_to(plugins_path.parent)
                    files["plugins"].append({
                        "source": str(item),
                        "relative": str(rel_path)
                    })

    if options.get("settings") and Path(dirs["settings"]).exists():
        files["settings"] = {
            "source": str(dirs["settings"]),
            "relative": "settings.json"
        }

    if options.get("projects"):
        files["projects"] = []
        for proj_dir in dirs["projects"]:
            proj_path = Path(proj_dir)
            claude_md = proj_path / "CLAUDE.md"
            if claude_md.exists():
                files["projects"].append({
                    "source": str(claude_md),
                    "relative": f"projects/{proj_path.name}/CLAUDE.md"
                })

    if options.get("scripts") and dirs.get("scripts"):
        files["scripts"] = []
        scripts_path = Path(dirs["scripts"])
        for script in scripts_path.rglob("*"):
            if script.is_file() and script.suffix in [".py", ".sh", ".js"]:
                rel_path = script.relative_to(scripts_path)
                files["scripts"].append({
                    "source": str(script),
                    "relative": str(rel_path)
                })

    return files

def get_deploy_script():
    """Return the deployment script content."""
    return '''#!/usr/bin/env python3
"""Deploy a Claude config package."""

import argparse
import json
import zipfile
from pathlib import Path
import shutil

def deploy_package(zip_path, target_dir, mode="merge", interactive=False):
    """Deploy a package to target directory."""
    zip_path = Path(zip_path).expanduser()
    target = Path(target_dir).expanduser()

    if not zip_path.exists():
        raise FileNotFoundError(f"Package not found: {zip_path}")

    target.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zf:
        manifest = json.loads(zf.read("manifest.json"))

        print(f"Deploying from: {zip_path}")
        print(f"Target: {target}")
        print(f"Mode: {mode}")
        print()
        print("Contents:")
        for key, count in manifest.get("contents", {}).items():
            print(f"  {key}: {count} files")
        print()

        if interactive:
            # Let user choose what to deploy
            print("What would you like to deploy?")
            options = {
                "skills": "[S]kills",
                "agents": "[A]gents",
                "plugins": "[P]lugins",
                "settings": "settings ([T])",
                "projects": "pro[J]ects",
                "scripts": "[C]cripts"
            }
            for key, label in options.items():
                print(f"  {label}")

            choice = input("Enter letters (e.g., 'sap' for skills+agents+plugins): ").lower()

            to_deploy = {
                "skills": "s" in choice,
                "agents": "a" in choice,
                "plugins": "p" in choice,
                "settings": "t" in choice,
                "projects": "j" in choice,
                "scripts": "c" in choice
            }
        else:
            to_deploy = {
                "skills": True,
                "agents": True,
                "plugins": True,
                "settings": True,
                "projects": True,
                "scripts": True
            }

        if mode == "replace" and to_deploy.get("plugins"):
            # Clear existing plugins
            plugins_target = target / "plugins"
            if plugins_target.exists():
                confirm = input("This will delete existing plugins. Continue? [y/N]: ")
                if confirm.lower() != "y":
                    to_deploy["plugins"] = False
                else:
                    shutil.rmtree(plugins_target)
                    plugins_target.mkdir(parents=True, exist_ok=True)

        # Extract files
        for info in zf.infolist():
            if info.filename.endswith("/"):
                continue

            # Determine category from path
            if info.filename == "settings.json":
                category = "settings"
            elif info.filename.startswith("projects/"):
                category = "projects"
            elif info.filename.startswith("skills/"):
                category = "skills"
            elif info.filename.startswith("agents/"):
                category = "agents"
            elif info.filename.startswith("plugins/"):
                category = "plugins"
            elif info.filename.startswith("scripts/"):
                category = "scripts"
            else:
                category = None

            # Check if this category should be deployed
            if category and not to_deploy.get(category, True):
                continue

            # Extract
            extract_path = target / info.filename
            extract_path.parent.mkdir(parents=True, exist_ok=True)

            if mode == "merge" and extract_path.exists():
                # Skip existing files in merge mode
                print(f"  Skipping (exists): {info.filename}")
                continue

            extract_path.write_bytes(zf.read(info.filename))
            print(f"  Deployed: {info.filename}")

    print()
    print("Deployment complete!")
    return manifest

def main():
    parser = argparse.ArgumentParser(description="Deploy Claude config package")
    parser.add_argument("package", help="Path to ZIP package")
    parser.add_argument("--target", "-t", default="~/.claude", help="Target directory")
    parser.add_argument("--mode", "-m", choices=["merge", "replace"], default="merge",
                       help="Deployment mode")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Interactive selection")

    args = parser.parse_args()
    deploy_package(args.package, args.target, args.mode, args.interactive)

if __name__ == "__main__":
    main()
'''

def create_package(files, output_path, manifest):
    """Create ZIP package with collected files."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add manifest
        zf.writestr("manifest.json", json.dumps(manifest, indent=2))

        # Add deploy script
        deploy_script = get_deploy_script()
        zf.writestr("DEPLOY.py", deploy_script)

        # Add skills
        for skill in files.get("skills", []):
            zf.write(skill["source"], f"skills/{skill['relative']}")

        # Add agents
        for agent in files.get("agents", []):
            zf.write(agent["source"], f"agents/{agent['relative']}")

        # Add plugins
        for plugin in files.get("plugins", []):
            zf.write(plugin["source"], f"plugins/{plugin['relative']}")

        # Add settings
        if "settings" in files:
            zf.write(files["settings"]["source"], "settings.json")

        # Add projects
        for proj in files.get("projects", []):
            zf.write(proj["source"], proj["relative"])

        # Add scripts
        for script in files.get("scripts", []):
            zf.write(script["source"], f"scripts/{script['relative']}")

    return output

def deploy_package(zip_path, target_dir, mode="merge", interactive=False):
    """Deploy a package to target directory."""
    import subprocess

    zip_path = Path(zip_path).expanduser()
    target = Path(target_dir).expanduser()

    if not zip_path.exists():
        raise FileNotFoundError(f"Package not found: {zip_path}")

    # Extract DEPLOY.py and run it
    with zipfile.ZipFile(zip_path, 'r') as zf:
        if "DEPLOY.py" in zf.namelist():
            deploy_script = zf.read("DEPLOY.py")
            deploy_path = zip_path.parent / "DEPLOY.py"
            deploy_path.write_bytes(deploy_script)

            # Run the deploy script
            cmd = ["python3", str(deploy_path), str(zip_path),
                   "--target", str(target), "--mode", mode]
            if interactive:
                cmd.append("--interactive")

            subprocess.run(cmd)

            # Cleanup
            deploy_path.unlink()
        else:
            # Fallback: extract directly
            print("No DEPLOY.py found, extracting directly...")
            zf.extractall(target)

def main():
    parser = argparse.ArgumentParser(description="Package Claude configurations")
    parser.add_argument("--config", "-c", help="Claude config directory (overrides CLAUDE_CONFIG_DIR env var)")
    parser.add_argument("--output", "-o", help="Output ZIP path")
    parser.add_argument("--deploy", "-d", help="Deploy from ZIP path")
    parser.add_argument("--target", help="Deploy target directory (defaults to same as source)")
    parser.add_argument("--mode", "-m", choices=["merge", "replace"], default="merge")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--skills", action="store_true", help="Include skills")
    parser.add_argument("--agents", action="store_true", help="Include agents")
    parser.add_argument("--plugins", action="store_true", help="Include plugins")
    parser.add_argument("--settings", action="store_true", help="Include settings")
    parser.add_argument("--projects", action="store_true", help="Include projects")
    parser.add_argument("--scripts", action="store_true", help="Include scripts")

    args = parser.parse_args()

    # Override config dir if specified
    if args.config:
        os.environ["CLAUDE_CONFIG_DIR"] = str(Path(args.config).expanduser())

    if args.deploy:
        # Deploy mode
        target = args.target if args.target else get_claude_base_dir()
        deploy_package(args.deploy, target, args.mode, args.interactive)
    else:
        # Package mode
        dirs = find_claude_config_dirs()
        options = {
            "skills": args.skills,
            "agents": args.agents,
            "plugins": args.plugins,
            "settings": args.settings,
            "projects": args.projects,
            "scripts": args.scripts
        }
        files = collect_files(dirs, options)

        manifest = {
            "created": datetime.now().isoformat(),
            "contents": {k: len(v) if isinstance(v, list) else 1
                        for k, v in files.items() if v}
        }

        output = args.output or f"~/claude-config-{datetime.now().strftime('%Y%m%d')}.zip"
        output = Path(output).expanduser()

        create_package(files, output, manifest)
        print(f"Created package: {output}")
        print(f"Size: {output.stat().st_size / 1024:.1f} KB")
        print(f"Contents: {json.dumps(manifest, indent=2)}")

if __name__ == "__main__":
    main()
