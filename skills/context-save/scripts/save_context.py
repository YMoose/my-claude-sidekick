#!/usr/bin/env python3
"""Export current Claude Code session to a directory on disk.

Usage:
    python save_context.py --session-id <uuid>
    python save_context.py --session-id <uuid> -o <output_base_path>

Arguments:
    --session-id      — Session ID to export (required)
    -o/--output-base-path
                      — Optional target base directory.
                        Defaults to the current working directory when omitted.

Exit codes:
    0 — Success
    1 — Missing arguments / bad usage
    2 — JSONL file not found
    3 — Output directory could not be created or written
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", maxsplit=1)[0])
    parser.add_argument(
        "-o",
        "--output-base-path",
        dest="output_base_path",
        help="Base directory where <session-id>/ will be created (defaults to current working directory)",
    )
    parser.add_argument(
        "--session-id",
        required=True,
        help="Session ID to export.",
    )
    args = parser.parse_args()
    args.output_base_path = args.output_base_path or "."
    return args


def locate_jsonl(session_id: str, cwd: str) -> Path | None:
    """Find the JSONL transcript file for the given session."""
    sanitized = "-" + cwd.lstrip("/").replace("/", "-")
    direct = Path.home() / ".claude" / "projects" / sanitized / f"{session_id}.jsonl"
    if direct.is_file():
        return direct

    projects_dir = Path.home() / ".claude" / "projects"
    if projects_dir.is_dir():
        for jsonl in projects_dir.rglob(f"{session_id}.jsonl"):
            return jsonl

    return None


def describe_session_dir(path: Path) -> tuple[bool, str]:
    if not path.is_dir():
        return False, "not found"

    subagents_dir = path / "subagents"
    subagent_count = sum(1 for f in subagents_dir.glob("*.jsonl") if f.is_file()) if subagents_dir.is_dir() else 0

    tool_results_dir = path / "tool-results"
    tool_result_count = sum(1 for f in tool_results_dir.rglob("*") if f.is_file()) if tool_results_dir.is_dir() else 0

    details: list[str] = []
    if subagent_count:
        details.append(f"{subagent_count} sub-agent transcript(s)")
    if tool_result_count:
        details.append(f"{tool_result_count} tool-result file(s)")
    if not details:
        details.append("no sub-agent or tool-result files")

    return True, "present with " + " and ".join(details)


def main() -> None:
    args = parse_args()

    cwd = os.getcwd()
    jsonl_path = locate_jsonl(args.session_id, cwd)

    if jsonl_path is None:
        print(f"ERROR: JSONL file not found for session {args.session_id}", file=sys.stderr)
        sanitized = "-" + cwd.lstrip("/").replace("/", "-")
        direct = Path.home() / ".claude" / "projects" / sanitized
        print(f"  Searched: {direct}/{args.session_id}.jsonl", file=sys.stderr)
        print(f"  Also searched: ~/.claude/projects/**/{args.session_id}.jsonl", file=sys.stderr)
        print(file=sys.stderr)
        print("Available session files in current project:", file=sys.stderr)
        if direct.is_dir():
            for file_path in sorted(direct.glob("*.jsonl")):
                print(f"  {file_path.name}", file=sys.stderr)
        else:
            print("  (none found)", file=sys.stderr)
        sys.exit(2)

    session_dir = jsonl_path.with_suffix("")
    output_base = Path(args.output_base_path).expanduser().resolve()
    output_dir = output_base / args.session_id

    if output_dir.exists() and any(output_dir.iterdir()):
        print(f"WARNING: Output directory already exists and will be updated in place: {output_dir}", file=sys.stderr)

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(jsonl_path, output_dir / jsonl_path.name)

        if session_dir.is_dir():
            shutil.copytree(session_dir, output_dir / session_dir.name, dirs_exist_ok=True)

        session_dir_present, session_dir_desc = describe_session_dir(output_dir / session_dir.name)
    except OSError as exc:
        print(f"ERROR: Could not write export to: {output_dir}", file=sys.stderr)
        print(f"  {exc}", file=sys.stderr)
        print("  Suggest using /tmp/ or a writable directory under your home folder.", file=sys.stderr)
        sys.exit(3)

    print(f"SUCCESS: Session context saved to: {output_dir}")
    print()
    print("Exported:")
    print(f"  - Transcript: {jsonl_path.name}")
    print(f"  - Session dir: {session_dir_desc if session_dir_present else 'not found'}")


if __name__ == "__main__":
    main()
