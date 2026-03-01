#!/usr/bin/env python3
"""
Validate YAML frontmatter in SKILL.md files.

Usage: python validate_frontmatter.py <path_to_skill.md>
"""

import sys
import re
import os


def validate_frontmatter(filepath: str) -> bool:
    """Validate the YAML frontmatter of a SKILL.md file."""

    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract frontmatter (between first two ---)
    if not content.startswith('---'):
        print("ERROR: File must start with '---'")
        return False

    parts = content.split('---', 2)
    if len(parts) < 3:
        print("ERROR: Invalid frontmatter structure (need opening and closing '---')")
        return False

    frontmatter = parts[1].strip()

    # Parse name field
    name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
    if not name_match:
        print("ERROR: Missing 'name' field in frontmatter")
        return False

    name = name_match.group(1).strip()

    # Validate name
    errors = []

    # Max 64 characters
    if len(name) > 64:
        errors.append(f"Name exceeds 64 characters (current: {len(name)})")

    # Only lowercase letters, numbers, and hyphens
    if not re.match(r'^[a-z0-9-]+$', name):
        errors.append("Name must contain only lowercase letters, numbers, and hyphens")

    # Check for XML tags
    if '<' in name or '>' in name:
        errors.append("Name cannot contain XML tags")

    # Check for reserved words
    reserved_words = ['anthropic', 'claude']
    for reserved in reserved_words:
        if reserved in name.lower():
            errors.append(f"Name cannot contain reserved word: '{reserved}'")

    # Parse description field
    desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
    if not desc_match:
        errors.append("Missing 'description' field in frontmatter")
        desc = ""
    else:
        desc = desc_match.group(1).strip()

        # Validate description
        if not desc:
            errors.append("Description must be non-empty")
        elif len(desc) > 1024:
            errors.append(f"Description exceeds 1024 characters (current: {len(desc)})")

        # Check for XML tags
        if '<' in desc or '>' in desc:
            errors.append("Description cannot contain XML tags")

    # Report results
    if errors:
        print(f"\nValidation FAILED for: {filepath}")
        print("=" * 50)
        for error in errors:
            print(f"  - {error}")
        return False

    print(f"\nValidation PASSED for: {filepath}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_frontmatter.py <path_to_skill.md>")
        sys.exit(1)

    filepath = sys.argv[1]
    success = validate_frontmatter(filepath)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
