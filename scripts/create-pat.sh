#!/bin/bash
# Create GitHub PAT with packages scope

# Check if curl is available
if ! command -v curl &> /dev/null; then
    echo "Error: curl is required but not installed."
    exit 1
fi

echo "=== Creating GitHub Personal Access Token (PAT) ==="
echo ""
echo "Required scopes:"
echo "  - read:packages"
echo "  - write:packages"
echo ""

echo "To create a PAT manually, visit:"
echo "https://github.com/settings/tokens"
echo ""
echo "Required scopes:"
echo "  - read:packages"
echo "  - write:packages"
echo ""
echo "After creating the token, run:"
echo 'export GITHUB_TOKEN="your-new-token-here"'
exit 0
