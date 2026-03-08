---
name: package-assets
description: |
  How to package and deploy Claude configurations (skills, agents, plugins) between machines.

  Use this skill whenever the user mentions:
  - Packaging, backing up, or exporting their Claude setup
  - Deploying configs to another machine
  - Sharing skills/agents/plugins with teammates
  - "zip my claude config", "export my skills", "backup my plugins"
  - Setting up Claude on a new machine with existing configs

  The skill provides interactive menus to select what to include and handles both packaging and deployment.
---

# Claude Packager

This skill helps you package your Claude configurations into a portable ZIP file and deploy them to other machines.

## What Can Be Packaged

- **Skills** - All `.md` skill definitions from `~/.claude/skills/` and plugin directories
- **Agents** - All agent definitions from `~/.claude/agents/` and plugin directories
- **Plugins** - All installed plugins from `~/.claude/plugins/` (cache and marketplaces)
- **Settings** - User preferences from `~/.claude/settings.json`
- **Project configs** - `CLAUDE.md` files from project directories
- **Custom scripts** - Any scripts in `~/.claude/scripts/`

Note: MCP configurations are NOT included as they often contain machine-specific paths and secrets.

## Usage

### Pack Mode (Export)

When the user wants to package their configs:

1. **Present the selection menu** - Show the user what can be included:
   ```
   What would you like to package?
   - [ ] Skills (*.md files)
   - [ ] Agents (agent definitions)
   - [ ] Plugins (installed plugins)
   - [ ] Settings (settings.json)
   - [ ] Project configs (CLAUDE.md files)
   - [ ] Custom scripts
   ```

2. **Find the source directories** - Use these default paths:
   - Skills: `~/.claude/skills/` (if exists) + plugin skills
   - Agents: `~/.claude/agents/` (if exists) + plugin agents
   - Plugins: `~/.claude/plugins/cache/` and `~/.claude/plugins/marketplaces/`
   - Settings: `~/.claude/settings.json`
   - Project configs: `~/.claude/projects/` (find all CLAUDE.md)
   - Scripts: `~/.claude/scripts/` (if exists)

3. **Create the package** - Run the packaging script with selected options

4. **Report the result** - Tell the user where the ZIP was created and its size.

### Deploy Mode (Import)

When the user wants to deploy a package:

1. **Get the ZIP path** - Ask for or locate the package file

2. **Preview contents** - Show what's in the package:
   ```bash
   unzip -l <package.zip>
   ```

3. **Present deployment options**:
   ```
   Where should configs be deployed?
   - Default: ~/.claude/ (merges with existing)
   - Custom path: [user specifies]

   Deployment mode:
   - Merge: Add new files, keep existing
   - Replace: Overwrite existing files (plugins only)
   - Interactive: Choose each file
   ```

4. **Run deployment** - Extract and place files appropriately

5. **Verify deployment** - Check that files were placed correctly

## Packaging Script

Create this script at `~/.claude/scripts/package_claude_config.py`:

```python
#!/usr/bin/env python3
"""Package Claude configurations into a ZIP file."""

import argparse
import json
import os
import zipfile
from pathlib import Path
from datetime import datetime
import shutil

def find_claude_config_dirs(config_base=None):
    """Find all relevant Claude config directories."""
    base = Path(config_base).expanduser() if config_base else Path.home() / ".claude"

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

            # Determine category
            parts = info.filename.split("/")
            if len(parts) < 2:
                continue

            category = parts[0].lower() if not info.filename.endswith(".json") else None
            if info.filename == "settings.json":
                category = "settings"
            elif info.filename.startswith("projects/"):
                category = "projects"

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
            cmd = ["python", str(deploy_path), str(zip_path),
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
    parser.add_argument("--config", "-c", help="Custom Claude config directory (default: ~/.claude)")
    parser.add_argument("--output", "-o", help="Output ZIP path")
    parser.add_argument("--deploy", "-d", help="Deploy from ZIP path")
    parser.add_argument("--target", "-t", default="~/.claude", help="Deploy target")
    parser.add_argument("--mode", "-m", choices=["merge", "replace"], default="merge")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--skills", action="store_true", help="Include skills")
    parser.add_argument("--agents", action="store_true", help="Include agents")
    parser.add_argument("--plugins", action="store_true", help="Include plugins")
    parser.add_argument("--settings", action="store_true", help="Include settings")
    parser.add_argument("--projects", action="store_true", help="Include projects")
    parser.add_argument("--scripts", action="store_true", help="Include scripts")

    args = parser.parse_args()

    if args.deploy:
        # Deploy mode
        deploy_package(args.deploy, args.target, args.mode, args.interactive)
    else:
        # Package mode
        dirs = find_claude_config_dirs(config_base=args.config)
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
```

## Step-by-Step Workflow

### For Packaging:

1. **Understand what the user wants** - Ask what they want to include if not specified
2. **Show the selection menu** - Present options interactively
3. **Scan for available files** - Use `find` commands to locate skills, agents, plugins
4. **Confirm selection** - Show summary of what will be included
5. **Create the script if needed** - Write `package_claude_config.py` to `~/.claude/scripts/`
6. **Run the packaging** - Execute the script with selected options
7. **Report results** - Show output path and size

### For Deployment:

1. **Get the package path** - Ask user or search for recent ZIP files
2. **Preview contents** - List what's in the package
3. **Ask for deployment preferences** - Target path and merge mode
4. **Run deployment** - Either:
   - Use the bundled DEPLOY.py script (preferred)
   - Or extract manually with `unzip`
5. **Verify** - Confirm files are in place

## Example Interactions

**User**: "I want to backup my claude setup"
**You**:
1. Present selection menu with all options
2. User confirms what to include
3. Create the packaging script at `~/.claude/scripts/package_claude_config.py`
4. Run: `python ~/.claude/scripts/package_claude_config.py --skills --agents --plugins -o ~/claude-backup.zip`
5. Report: "Created ~/claude-backup.zip (2.4 MB) with 12 skills, 8 agents, and 15 plugins"

**User**: "How do I deploy this on my other machine?"
**You**:
1. Guide them to copy the ZIP to the target machine
2. Run: `python claude-backup.zip/DEPLOY.py claude-backup.zip --target ~/.claude --mode merge`
3. Or: `python ~/.claude/scripts/package_claude_config.py --deploy claude-backup.zip --target ~/.claude`
4. Verify deployment

**User**: "I want to share my skills with my team"
**You**:
1. Package their skills (and optionally agents/plugins)
2. Tell them to share the ZIP file
3. Teammates run the deploy command on their machines

## Tips

- Always show users what will be included before packaging
- Warn about potentially sensitive data in settings.json (API keys, tokens)
- For large packages, mention the size
- When deploying, prefer "merge" mode to avoid losing existing configs
- The DEPLOY.py script is bundled in every package for easy deployment
- Keep the package script at `~/.claude/scripts/` for reuse

## Quick Commands

```bash
# Package everything
python ~/.claude/scripts/package_claude_config.py --skills --agents --plugins --settings -o claude-full.zip

# Package just skills and agents
python ~/.claude/scripts/package_claude_config.py --skills --agents -o claude-skills.zip

# Deploy with merge (default)
python ~/.claude/scripts/package_claude_config.py --deploy claude-full.zip

# Deploy to custom location
python ~/.claude/scripts/package_claude_config.py --deploy claude-full.zip --target /path/to/custom

# Interactive deployment (choose what to install)
python ~/.claude/scripts/package_claude_config.py --deploy claude-full.zip --interactive

# Custom config directory (e.g., /opt/claude/config)
python ~/.claude/scripts/package_claude_config.py --config /opt/claude/config --skills --output ~/backup.zip
```

## Custom Config Directory

If your Claude configs are stored in a non-default location (e.g., `/opt/claude/config` instead of `~/.claude/`), use the `--config` flag:

```bash
# Backup skills from custom config location
python ~/.claude/scripts/package_claude_config.py --config /opt/claude/config --skills --output ~/claude-skills-backup.zip

# Backup everything from custom config location
python ~/.claude/scripts/package_claude_config.py --config /opt/claude/config --skills --agents --plugins --settings --projects --scripts --output ~/claude-full-backup.zip

# Deploy to custom config location
python ~/.claude/scripts/package_claude_config.py --deploy claude-backup.zip --target /opt/claude/config --mode merge
```
