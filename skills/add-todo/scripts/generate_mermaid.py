#!/usr/bin/env python3
"""
Generate mermaid flowchart from YAML/JSON data.

Usage:
    python generate_mermaid.py '<yaml_or_json_string>'

Reads YAML nodes and relations and outputs mermaid flowchart.
"""

import sys
import re
import json
from typing import List, Dict, Tuple
from datetime import datetime


def parse_yaml(yaml_str: str) -> Tuple[List[Dict], List[Tuple[str, str]]]:
    """Parse YAML nodes and relations from string."""
    nodes = []
    relations = []

    lines = yaml_str.split('\n')
    current_node = None
    in_nodes = False
    in_relations = False

    for line in lines:
        stripped = line.strip()

        if stripped == 'nodes:':
            in_nodes = True
            in_relations = False
            continue
        elif stripped == 'relations:':
            in_nodes = False
            in_relations = True
            continue

        if in_nodes:
            node_match = re.match(r'-\s*"([^"]+)":', stripped)
            if node_match:
                if current_node:
                    nodes.append(current_node)
                current_node = {"name": node_match.group(1)}
            elif current_node:
                prop_match = re.match(r'(\w+):\s*(.*)', stripped)
                if prop_match:
                    current_node[prop_match.group(1)] = prop_match.group(2).strip()

        elif in_relations:
            rel_match = re.match(r'-\s*\[\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\]', stripped)
            if rel_match:
                relations.append((rel_match.group(1), rel_match.group(2)))

    if current_node:
        nodes.append(current_node)

    return nodes, relations


def parse_json(json_str: str) -> Tuple[List[Dict], List[Tuple[str, str]]]:
    """Parse JSON nodes and relations from string."""
    data = json.loads(json_str)
    nodes = data.get("nodes", [])
    relations = []
    for r in data.get("relations", []):
        if len(r) >= 2:
            relations.append((r[0], r[1]))
    return nodes, relations


def generate_node_id(index: int, create_time: str = None) -> str:
    """Generate unique node ID from create_time or current time."""
    if create_time:
        # Parse date like "2026-02-25" and convert to YYYYMMDD format
        try:
            dt = datetime.strptime(create_time, "%Y-%m-%d")
            timestamp = dt.strftime("%Y%m%d")
        except ValueError:
            timestamp = datetime.now().strftime("%Y%m%d")
    else:
        timestamp = datetime.now().strftime("%Y%m%d")
    return f"{timestamp}_{index}"


def generate_mermaid(nodes: List[Dict], relations: List[Tuple[str, str]]) -> str:
    """Generate mermaid flowchart from nodes and relations."""
    lines = ["flowchart TD"]

    name_to_id = {}
    for i, node in enumerate(nodes):
        create_time = node.get("create_time")
        node_id = generate_node_id(i, create_time)
        name = node.get("name", node.get("task", ""))
        name_to_id[name] = node_id
        safe_name = name.replace('"', "'")
        lines.append(f'    {node_id}["{safe_name}"]')

    lines.append("")

    for from_task, to_task in relations:
        from_id = name_to_id.get(from_task)
        to_id = name_to_id.get(to_task)
        if from_id and to_id:
            lines.append(f'    {from_id} --> {to_id}')

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_mermaid.py '<yaml_or_json_string>'")
        sys.exit(1)

    input_str = sys.argv[1]

    # Try JSON first, then YAML
    try:
        nodes, relations = parse_json(input_str)
    except json.JSONDecodeError:
        nodes, relations = parse_yaml(input_str)

    if not nodes:
        print("Error: No nodes found in input")
        sys.exit(1)

    print(generate_mermaid(nodes, relations))


if __name__ == "__main__":
    main()
