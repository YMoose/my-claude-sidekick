#!/usr/bin/env python3
"""
Integrate Google Scholar search results into the sample.json format.

Usage:
    python integrate_results.py results.json -o sample.json
    python integrate_results.py results.json  # outputs to integrated_sample.json
    python integrate_results.py results.json --append sample.json -o sample.json
"""

import json
import argparse
import os
from pathlib import Path
from typing import Optional


def load_json(filepath: str) -> dict:
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: dict, filepath: str):
    """Save data to JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def convert_result_to_paper(result: dict, new_id: int) -> dict:
    """Convert a Google Scholar result to the sample.json paper format."""
    paper = {
        "id": new_id,
        "url": result.get("url", ""),
        "eprint_url": result.get("eprint_url", ""),
        "title": result.get("title", ""),
        "year": int(result.get("year", 0)) if result.get("year") else 0,
        "authors": result.get("authors", ""),
        "venue": result.get("venue", ""),
        "citations": result.get("citations", 0),
        "cited": [],  # Always empty for new papers
        "abstract": result.get("abstract", "")
    }

    # Remove empty fields
    if not paper["url"]:
        del paper["url"]
    if not paper["eprint_url"]:
        del paper["eprint_url"]
    if not paper["abstract"]:
        del paper["abstract"]

    return paper


def get_next_id(existing_papers: list) -> int:
    """Get the next available ID."""
    if not existing_papers:
        return 1
    return max(p.get("id", 0) for p in existing_papers) + 1


def check_title_similarity(title1: str, title2: str, threshold: float = 0.8) -> bool:
    """Check if two titles are similar (simple word overlap check)."""
    if not title1 or not title2:
        return False

    words1 = set(title1.lower().split())
    words2 = set(title2.lower().split())

    # Remove common words
    common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
    words1 = words1 - common_words
    words2 = words2 - common_words

    if not words1 or not words2:
        return False

    intersection = words1 & words2
    union = words1 | words2

    similarity = len(intersection) / len(union) if union else 0
    return similarity >= threshold


def find_duplicate(paper: dict, existing_papers: list) -> Optional[dict]:
    """Find if a paper already exists in the list (by title similarity)."""
    title = paper.get("title", "")

    for existing in existing_papers:
        if check_title_similarity(title, existing.get("title", "")):
            return existing

    return None


def integrate_results(scholar_data: dict, existing_data: Optional[dict] = None,
                      skip_duplicates: bool = True) -> dict:
    """
    Integrate Google Scholar results into existing data.

    Args:
        scholar_data: Data from Google Scholar search
        existing_data: Existing sample.json data (can be None)
        skip_duplicates: Skip papers that already exist

    Returns:
        Integrated data in sample.json format
    """
    # Initialize or use existing data
    if existing_data is None:
        integrated = {"data": []}
    else:
        integrated = {"data": list(existing_data.get("data", []))}

    existing_papers = integrated["data"]
    next_id = get_next_id(existing_papers)

    # Get results from scholar data
    results = scholar_data.get("results", [])

    added_count = 0
    skipped_count = 0

    for result in results:
        # Check for duplicates
        duplicate = find_duplicate(result, existing_papers)

        if duplicate and skip_duplicates:
            print(f"  Skipping duplicate: {result.get('title', 'Unknown')[:50]}...")
            skipped_count += 1
            continue

        # Convert and add paper
        new_paper = convert_result_to_paper(result, next_id)
        existing_papers.append(new_paper)
        next_id += 1
        added_count += 1

    # Sort by year (descending) then by citations (descending)
    integrated["data"].sort(key=lambda p: (p.get("year", 0), p.get("citations", 0)), reverse=True)

    # Re-assign IDs after sorting and clear all cited fields
    for i, paper in enumerate(integrated["data"], 1):
        paper["id"] = i
        paper["cited"] = []  # Keep cited field empty

    print(f"\nSummary:")
    print(f"  Added: {added_count}")
    print(f"  Skipped (duplicates): {skipped_count}")
    print(f"  Total papers: {len(integrated['data'])}")

    return integrated


def main():
    parser = argparse.ArgumentParser(
        description='Integrate Google Scholar search results into sample.json format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    # Create new file from results
    python integrate_results.py results.json -o integrated.json

    # Append to existing sample.json
    python integrate_results.py results.json --append sample.json -o sample.json

    # Include duplicates
    python integrate_results.py results.json --no-skip-duplicates -o output.json
        '''
    )

    parser.add_argument('input', help='Input Google Scholar results JSON file')
    parser.add_argument('-o', '--output', help='Output JSON file (default: integrated_sample.json)',
                        default='integrated_sample.json')
    parser.add_argument('--append', help='Existing sample.json to append to', default=None)
    parser.add_argument('--no-skip-duplicates', action='store_true',
                        help='Include duplicate papers (default: skip)')

    args = parser.parse_args()

    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' not found")
        return 1

    # Load scholar results
    print(f"Loading Google Scholar results from {args.input}...")
    try:
        scholar_data = load_json(args.input)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        return 1

    # Load existing data if appending
    existing_data = None
    if args.append:
        append_path = Path(args.append)
        if append_path.exists():
            print(f"Loading existing data from {args.append}...")
            try:
                existing_data = load_json(args.append)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in append file - {e}")
                return 1
        else:
            print(f"Warning: Append file '{args.append}' not found, creating new file")

    # Integrate results
    print(f"\nIntegrating {len(scholar_data.get('results', []))} results...")
    integrated = integrate_results(
        scholar_data,
        existing_data,
        skip_duplicates=not args.no_skip_duplicates
    )

    # Save output
    save_json(integrated, args.output)
    print(f"\nSaved to {args.output}")

    return 0


if __name__ == '__main__':
    exit(main())
