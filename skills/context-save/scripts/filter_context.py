#!/usr/bin/env python3
"""List anchor candidates or filter an exported Claude session by anchor.

Usage:
    python3 scripts/filter_context.py <saved-session-dir> --list-anchors
    python3 scripts/filter_context.py <saved-session-dir> --anchor-uuid <uuid>
    python3 scripts/filter_context.py <saved-session-dir> --anchor-uuid <uuid> -o <output-dir>

Arguments:
    saved_session_dir  — Directory previously exported by save_context.py.
    --list-anchors     — Print valid anchor candidates as JSON without modifying files.
    --anchor-uuid      — Anchor UUID to keep when filtering.
    -o/--output-dir    — Optional output base directory.
                         The filtered result is written to <output-dir>/<session-id>/.
                         Defaults to the current working directory when omitted.

Exit codes:
    0 — Success
    1 — Exported session could not be read or filtered
    2 — Missing arguments / bad usage
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

TRANSCRIPT_TYPES = {"user", "assistant", "attachment", "system"}
TOOL_RESULT_FILENAMES_PATTERN = re.compile(
    r"(?:^|[\\/])(call_[A-Za-z0-9]+(?:\.[A-Za-z0-9._-]+)?|[A-Za-z0-9._-]+\.(?:txt|json))(?=$|[\s\"'<>])"
)
TASK_ID_TAG_PATTERN = re.compile(r"<task-id>([^<]+)</task-id>")
AGENT_ID_PATTERNS = [
    re.compile(r'"agentId"\s*:\s*"([^"]+)"'),
    re.compile(r'"task_id"\s*:\s*"([^"]+)"'),
    re.compile(r"\bagentId:\s*([A-Za-z0-9-]+)"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("saved_session_dir", help="Directory created by save_context.py")
    parser.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        help=(
            "Output base directory for the filtered session. "
            "The result is written to <output-dir>/<saved-session-dir-name>/ "
            "(defaults to the current working directory)."
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--list-anchors", action="store_true", help="Print anchor candidates as JSON")
    mode.add_argument("--anchor-uuid", help="UUID of the anchor message to keep from")
    args = parser.parse_args()
    args.output_dir = args.output_dir or "."
    return args


def main() -> None:
    args = parse_args()
    saved_session_dir = Path(args.saved_session_dir).expanduser().resolve()
    transcript_path, companion_dir = locate_export_artifacts(saved_session_dir)
    entries = load_entries(transcript_path)
    transcript_entries = [entry for entry in entries if is_transcript_entry(entry["data"])]

    if not transcript_entries:
        raise SystemExit("ERROR: No transcript messages with UUIDs were found in the exported JSONL.")

    if args.list_anchors:
        candidates = list_anchor_candidates(entries)
        print(json.dumps(candidates, ensure_ascii=False, indent=2))
        return

    output_base_dir = Path(args.output_dir).expanduser().resolve()
    output_dir = output_base_dir / saved_session_dir.name
    filter_export(
        saved_session_dir=saved_session_dir,
        output_dir=output_dir,
        transcript_path=transcript_path,
        companion_dir=companion_dir,
        entries=entries,
        anchor_uuid=args.anchor_uuid,
    )


def locate_export_artifacts(saved_session_dir: Path) -> tuple[Path, Path | None]:
    if not saved_session_dir.is_dir():
        raise SystemExit(f"ERROR: Saved session directory not found: {saved_session_dir}")

    jsonl_files = sorted(
        path for path in saved_session_dir.iterdir() if path.is_file() and path.suffix == ".jsonl"
    )
    if not jsonl_files:
        raise SystemExit(f"ERROR: No top-level transcript JSONL found in: {saved_session_dir}")

    transcript_path: Path | None = None
    if len(jsonl_files) == 1:
        transcript_path = jsonl_files[0]
    else:
        by_name = {path.stem: path for path in jsonl_files}
        transcript_path = by_name.get(saved_session_dir.name)
        if transcript_path is None:
            for path in jsonl_files:
                if (saved_session_dir / path.stem).is_dir():
                    transcript_path = path
                    break
    if transcript_path is None:
        names = ", ".join(path.name for path in jsonl_files)
        raise SystemExit(
            f"ERROR: Found multiple JSONL files in {saved_session_dir} and could not infer the main transcript: {names}"
        )

    companion_dir = saved_session_dir / transcript_path.stem
    return transcript_path, companion_dir if companion_dir.is_dir() else None


def load_entries(transcript_path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    with transcript_path.open("r", encoding="utf-8") as handle:
        for idx, raw_line in enumerate(handle):
            line = raw_line.rstrip("\n")
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"ERROR: Invalid JSON at {transcript_path}:{idx + 1}: {exc}") from exc
            entries.append({"index": idx, "line_number": idx + 1, "data": data})
    return entries


def is_transcript_entry(entry: dict[str, Any]) -> bool:
    return entry.get("type") in TRANSCRIPT_TYPES and isinstance(entry.get("uuid"), str)


def flatten_message_text(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                item_type = item.get("type")
                if item_type == "text" and isinstance(item.get("text"), str):
                    parts.append(item["text"])
                elif item_type == "tool_result":
                    content_value = item.get("content")
                    if isinstance(content_value, str):
                        parts.append(content_value)
        return "\n".join(part.strip() for part in parts if part).strip()
    return ""


def is_tool_result_user(entry: dict[str, Any]) -> bool:
    if entry.get("type") != "user":
        return False
    content = entry.get("message", {}).get("content")
    if not isinstance(content, list):
        return False
    return any(isinstance(item, dict) and item.get("type") == "tool_result" for item in content)


def candidate_kind(entry: dict[str, Any]) -> str | None:
    if entry.get("type") != "user" or not isinstance(entry.get("uuid"), str):
        return None
    if entry.get("isMeta"):
        return None
    if is_tool_result_user(entry):
        return None

    text = flatten_message_text(entry.get("message", {}).get("content"))
    if entry.get("isCompactSummary"):
        return "compact-summary"
    if "<command-message>" in text:
        return "command-message"
    if text.startswith("<ide_opened_file>") or text.startswith("<ide_selection>"):
        return None
    if text.startswith("<task-notification>") or text.startswith("[Request interrupted by user]"):
        return None
    if text.startswith("<"):
        return None
    return "user-message" if text else None


def build_preview(text: str, limit: int = 160) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= limit else flat[: limit - 1].rstrip() + "…"


def list_anchor_candidates(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for wrapper in entries:
        entry = wrapper["data"]
        kind = candidate_kind(entry)
        if not kind:
            continue
        text = flatten_message_text(entry.get("message", {}).get("content"))
        candidates.append(
            {
                "uuid": entry["uuid"],
                "line_number": wrapper["line_number"],
                "timestamp": entry.get("timestamp"),
                "kind": kind,
                "preview": build_preview(text),
            }
        )
    return candidates


def filter_export(
    *,
    saved_session_dir: Path,
    output_dir: Path,
    transcript_path: Path,
    companion_dir: Path | None,
    entries: list[dict[str, Any]],
    anchor_uuid: str,
) -> None:
    in_place = output_dir == saved_session_dir
    if not in_place and output_dir.exists() and any(output_dir.iterdir()):
        raise SystemExit(f"ERROR: Output directory already exists and is not empty: {output_dir}")

    transcript_entries = [wrapper for wrapper in entries if is_transcript_entry(wrapper["data"])]
    entry_by_uuid = {wrapper["data"]["uuid"]: wrapper for wrapper in transcript_entries}
    anchor_wrapper = entry_by_uuid.get(anchor_uuid)
    if anchor_wrapper is None:
        raise SystemExit(f"ERROR: Anchor UUID was not found in transcript messages: {anchor_uuid}")

    if candidate_kind(anchor_wrapper["data"]) is None:
        raise SystemExit(
            "ERROR: Anchor UUID is not a valid conversation-block start. "
            "Use --list-anchors to choose a user message, command message, or compact-summary anchor."
        )

    first_transcript_wrapper = transcript_entries[0]
    root_uuid = first_transcript_wrapper["data"]["uuid"]
    keep_root = anchor_uuid != root_uuid

    children: dict[str, list[str]] = defaultdict(list)
    for wrapper in transcript_entries:
        parent_uuid = wrapper["data"].get("parentUuid")
        if isinstance(parent_uuid, str):
            children[parent_uuid].append(wrapper["data"]["uuid"])

    kept_descendants = collect_descendants(anchor_uuid, children)
    kept_transcript_ids = set(kept_descendants)
    if keep_root:
        kept_transcript_ids.add(root_uuid)

    anchor_index = anchor_wrapper["index"]
    baseline_wrapper: dict[str, Any] | None = None
    for wrapper in entries:
        if wrapper["index"] >= anchor_index:
            break
        if wrapper["data"].get("type") == "file-history-snapshot":
            baseline_wrapper = wrapper

    baseline_series_id = None
    if baseline_wrapper is not None:
        baseline_series_id = baseline_wrapper["data"].get("snapshot", {}).get("messageId")

    filtered_entries: list[dict[str, Any]] = []
    first_transcript_index = first_transcript_wrapper["index"]

    for wrapper in entries:
        idx = wrapper["index"]
        entry = wrapper["data"]

        if baseline_wrapper is not None and idx == baseline_wrapper["index"]:
            filtered_entries.append(rewrite_baseline_snapshot(entry, anchor_uuid))
            continue

        if idx < first_transcript_index:
            if entry.get("type") != "file-history-snapshot":
                filtered_entries.append(clone_entry(entry))
            continue

        if is_transcript_entry(entry):
            uuid = entry["uuid"]
            if uuid not in kept_transcript_ids:
                continue
            copied = clone_entry(entry)
            if uuid == anchor_uuid and keep_root:
                copied["parentUuid"] = root_uuid
            filtered_entries.append(copied)
            continue

        if entry.get("type") == "file-history-snapshot":
            message_id = entry.get("messageId")
            if wrapper["index"] < anchor_index:
                continue
            if message_id not in kept_transcript_ids:
                continue
            copied = clone_entry(entry)
            if (
                baseline_series_id is not None
                and copied.get("snapshot", {}).get("messageId") == baseline_series_id
            ):
                copied["snapshot"]["messageId"] = anchor_uuid
            filtered_entries.append(copied)

    if not filtered_entries:
        raise SystemExit("ERROR: Filtering removed every entry; no output was written.")

    target_dir = output_dir
    backup_dir: Path | None = None
    if in_place:
        target_dir = Path(
            tempfile.mkdtemp(prefix=f".{saved_session_dir.name}.filter-", dir=str(saved_session_dir.parent))
        )

    target_dir.mkdir(parents=True, exist_ok=True)
    output_transcript_path = target_dir / transcript_path.name
    write_jsonl(output_transcript_path, filtered_entries)

    kept_agent_ids = collect_agent_ids(filtered_entries)
    kept_tool_result_names = collect_tool_result_filenames(filtered_entries)

    target_session_dir: Path | None = None
    if companion_dir is not None:
        source_session_dir = companion_dir
        target_session_dir = target_dir / companion_dir.name
        if kept_agent_ids:
            copy_kept_subagent_files(
                source_session_dir=source_session_dir,
                target_session_dir=target_session_dir,
                kept_agent_ids=kept_agent_ids,
            )
            kept_tool_result_names.update(
                collect_tool_result_filenames_from_subagents(target_session_dir / "subagents")
            )
        copy_kept_tool_result_files(
            source_session_dir=source_session_dir,
            target_session_dir=target_session_dir,
            kept_tool_result_names=kept_tool_result_names,
        )

    if in_place:
        backup_dir = saved_session_dir.parent / f".{saved_session_dir.name}.pre-filter-backup"
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        saved_session_dir.rename(backup_dir)
        try:
            target_dir.rename(saved_session_dir)
        except Exception:
            if saved_session_dir.exists():
                shutil.rmtree(saved_session_dir)
            backup_dir.rename(saved_session_dir)
            raise
        shutil.rmtree(backup_dir)

    final_dir = saved_session_dir if in_place else output_dir
    final_session_dir = final_dir / companion_dir.name if companion_dir is not None else None
    session_dir_desc = describe_filtered_session_dir(companion_dir, final_session_dir)

    print(f"SUCCESS: Filtered session written to: {final_dir}")
    print()
    print("Filtered:")
    print(f"  - Transcript: {output_transcript_path.name} (filtered)")
    print(f"  - Session dir: {session_dir_desc}")
    print(f"  - Anchor UUID: {anchor_uuid}")


def collect_descendants(anchor_uuid: str, children: dict[str, list[str]]) -> list[str]:
    ordered: list[str] = []
    queue: deque[str] = deque([anchor_uuid])
    seen: set[str] = set()
    while queue:
        current = queue.popleft()
        if current in seen:
            continue
        seen.add(current)
        ordered.append(current)
        for child in children.get(current, []):
            queue.append(child)
    return ordered


def clone_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(entry, ensure_ascii=False))


def rewrite_baseline_snapshot(entry: dict[str, Any], anchor_uuid: str) -> dict[str, Any]:
    copied = clone_entry(entry)
    copied["messageId"] = anchor_uuid
    snapshot = copied.get("snapshot")
    if isinstance(snapshot, dict):
        snapshot["messageId"] = anchor_uuid
    copied["isSnapshotUpdate"] = False
    return copied


def write_jsonl(path: Path, entries: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")


def collect_agent_ids(entries: list[dict[str, Any]]) -> set[str]:
    agent_ids: set[str] = set()
    for entry in entries:
        text = json.dumps(entry, ensure_ascii=False, separators=(",", ":"))
        for pattern in AGENT_ID_PATTERNS:
            for match in pattern.findall(text):
                if match:
                    agent_ids.add(match)
        for match in TASK_ID_TAG_PATTERN.findall(text):
            if match:
                agent_ids.add(match)
    return agent_ids


def collect_tool_result_filenames(entries: list[dict[str, Any]]) -> set[str]:
    text = "\n".join(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) for entry in entries)
    return {match for match in TOOL_RESULT_FILENAMES_PATTERN.findall(text)}


def copy_kept_subagent_files(
    *,
    source_session_dir: Path,
    target_session_dir: Path,
    kept_agent_ids: set[str],
) -> None:
    source_subagents_dir = source_session_dir / "subagents"
    if not source_subagents_dir.is_dir():
        return

    for path in source_subagents_dir.rglob("*"):
        if not path.is_file():
            continue
        if not subagent_file_matches(path.name, kept_agent_ids):
            continue
        destination = target_session_dir / path.relative_to(source_session_dir)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)


def subagent_file_matches(filename: str, kept_agent_ids: set[str]) -> bool:
    for agent_id in kept_agent_ids:
        if filename == f"agent-{agent_id}.jsonl" or filename == f"agent-{agent_id}.meta.json":
            return True
    return False


def collect_tool_result_filenames_from_subagents(subagents_dir: Path) -> set[str]:
    if not subagents_dir.is_dir():
        return set()
    text_chunks: list[str] = []
    for path in subagents_dir.rglob("*.jsonl"):
        try:
            text_chunks.append(path.read_text(encoding="utf-8"))
        except OSError:
            continue
    text = "\n".join(text_chunks)
    return {match for match in TOOL_RESULT_FILENAMES_PATTERN.findall(text)}


def copy_kept_tool_result_files(
    *,
    source_session_dir: Path,
    target_session_dir: Path,
    kept_tool_result_names: set[str],
) -> None:
    source_tool_results_dir = source_session_dir / "tool-results"
    if not source_tool_results_dir.is_dir() or not kept_tool_result_names:
        return

    for path in source_tool_results_dir.rglob("*"):
        if not path.is_file() or path.name not in kept_tool_result_names:
            continue
        destination = target_session_dir / path.relative_to(source_session_dir)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)


def describe_filtered_session_dir(
    source_session_dir: Path | None, target_session_dir: Path | None
) -> str:
    if source_session_dir is None:
        return "not found"
    if target_session_dir is None or not target_session_dir.is_dir():
        return "not copied (no referenced sub-agent or tool-result files)"

    has_subagent_files = directory_has_files(target_session_dir / "subagents")
    has_tool_result_files = directory_has_files(target_session_dir / "tool-results")

    details: list[str] = []
    if has_subagent_files:
        details.append("kept sub-agent files")
    if has_tool_result_files:
        details.append("kept tool-result files")
    if not details:
        return "not copied (no referenced sub-agent or tool-result files)"
    return "present with " + " and ".join(details)


def directory_has_files(path: Path) -> bool:
    return path.is_dir() and any(child.is_file() for child in path.rglob("*"))


if __name__ == "__main__":
    main()
