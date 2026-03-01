#!/bin/bash
# Check for accidentally committed secrets in repository

echo "Kenkoumon Secret Scanner"
echo "========================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

found_issues=0

# Check for common secret patterns
echo "Scanning for potential secrets..."

# Patterns to check
patterns=(
    "sk-[a-zA-Z0-9]{20,}"           # OpenAI API keys
    "sk-ant-[a-zA-Z0-9]{20,}"       # Anthropic API keys
    "Bearer [a-zA-Z0-9]{20,}"       # Bearer tokens
    "password.*=.*[^$]"             # Password assignments
    "SECRET_KEY.*=.*[^$]"           # Secret key assignments (not env vars)
    "api.*key.*=.*[^$]"             # API key assignments (not env vars)
)

for pattern in "${patterns[@]}"; do
    matches=$(grep -rE "$pattern" . \
        --exclude-dir=.git \
        --exclude-dir=venv \
        --exclude-dir=node_modules \
        --exclude="*.pyc" \
        --exclude="*.db" \
        --exclude="secrets.env" \
        --exclude=".env.local" \
        --exclude="*.png" \
        --exclude="*.jpg" \
        --exclude="README.md" \
        --exclude="*.md" || true)

    if [ -n "$matches" ]; then
        echo -e "${RED}⚠️  Found potential secret matching: $pattern${NC}"
        echo "$matches"
        echo ""
        found_issues=1
    fi
done

# Check for committed .env files
if git ls-files | grep -q "\.env$"; then
    echo -e "${RED}⚠️  Found .env files tracked in git!${NC}"
    git ls-files | grep "\.env$"
    echo ""
    found_issues=1
fi

# Check for .env.local files
if git ls-files | grep -q "\.env.local$"; then
    echo -e "${RED}⚠️  Found .env.local files tracked in git!${NC}"
    git ls-files | grep "\.env.local$"
    echo ""
    found_issues=1
fi

# Check if secrets.env exists
if [ -f "secrets.env" ]; then
    if git ls-files | grep -q "secrets.env"; then
        echo -e "${RED}⚠️  secrets.env is tracked in git! Remove it immediately.${NC}"
        echo ""
        found_issues=1
    else
        echo -e "${GREEN}✓ secrets.env exists but is not tracked (good!)${NC}"
    fi
fi

# Check .gitignore
echo ""
echo "Checking .gitignore..."
required_ignores=(".env" ".env.local" "secrets.env" "*.key" "*.pem")

for ignore in "${required_ignores[@]}"; do
    if grep -q "^$ignore" .gitignore 2>/dev/null; then
        echo -e "${GREEN}✓ $ignore is ignored${NC}"
    else
        echo -e "${YELLOW}⚠️  $ignore is not in .gitignore${NC}"
        found_issues=1
    fi
done

echo ""
echo "========================"
if [ $found_issues -eq 0 ]; then
    echo -e "${GREEN}✓ No secret issues detected${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Issues found! Please review and fix.${NC}"
    exit 1
fi
