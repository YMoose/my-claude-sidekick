#!/bin/bash
# Install skill by creating a symlink
# Usage: ./install-skill.sh [skill-name] [target-skills-dir]
#
# This script creates a symlink from the skill source to ~/.claude/skills/

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
SKILL_NAME="${1:-package-assets}"
SKILLS_DIR="${2:-$HOME/.claude/skills}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SOURCE="$SCRIPT_DIR/skills/$SKILL_NAME"  # skills/<skill-name>/

# If skill-name is a path (contains /), use it directly
if [[ "$SKILL_NAME" == */* ]]; then
    SKILL_SOURCE="$SCRIPT_DIR/$SKILL_NAME"
fi

echo "Installing ${SKILL_NAME} skill..."
echo ""
echo "  Source: ${SKILL_SOURCE}"
echo "  Target: ${SKILLS_DIR}/${SKILL_NAME}"
echo ""

# Verify source exists
if [ ! -d "$SKILL_SOURCE" ]; then
    echo -e "${RED}Error: Source directory not found: $SKILL_SOURCE${NC}"
    exit 1
fi

# Verify source contains required files
if [ ! -f "$SKILL_SOURCE/SKILL.md" ]; then
    echo -e "${RED}Error: Source directory does not contain SKILL.md${NC}"
    exit 1
fi

# Create skills directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Check if skill is already installed
if [ -L "$SKILLS_DIR/$SKILL_NAME" ]; then
    echo -e "${YELLOW}Skill already installed (symlink exists). Removing old symlink...${NC}"
    rm "$SKILLS_DIR/$SKILL_NAME"
fi

if [ -d "$SKILLS_DIR/$SKILL_NAME" ] && [ ! -L "$SKILLS_DIR/$SKILL_NAME" ]; then
    echo -e "${RED}Error: A directory named '$SKILL_NAME' already exists in $SKILLS_DIR${NC}"
    echo -e "${YELLOW}Please remove it first: rm -rf $SKILLS_DIR/$SKILL_NAME${NC}"
    exit 1
fi

# Create symlink
ln -s "$SKILL_SOURCE" "$SKILLS_DIR/$SKILL_NAME"

# Verify
if [ -L "$SKILLS_DIR/$SKILL_NAME" ]; then
    echo ""
    echo -e "${GREEN}✓ Skill installed successfully!${NC}"
    echo ""
    echo "The skill is now available at: $SKILLS_DIR/$SKILL_NAME"
    echo ""
    echo "To uninstall:"
    echo "  unlink $SKILLS_DIR/$SKILL_NAME"
else
    echo -e "${RED}Error: Failed to create symlink${NC}"
    exit 1
fi
