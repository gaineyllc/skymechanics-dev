#!/bin/bash
# Check current GHCR storage usage

set -e

# Check if GITHUB_TOKEN is set
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GITHUB_TOKEN not set"
    echo "Set it with: export GITHUB_TOKEN=your-token-here"
    echo "Get a token from: https://github.com/settings/tokens"
    echo "Required scopes: read:packages, write:packages"
    exit 1
fi

echo "=== GHCR Storage Usage Check ==="
echo ""

# Get package list
echo "Fetching package list..."
PACKAGES=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
    https://api.github.com/users/gaineyllc/packages?per_page=100)

if echo "$PACKAGES" | grep -q "message"; then
    echo "Error: API returned: $(echo "$PACKAGES" | jq -r '.message')"
    exit 1
fi

echo "Packages found: $(echo "$PACKAGES" | jq 'length')"
echo ""

# Calculate total storage
TOTAL_BYTES=0
TOTAL_MB=0

echo "Package sizes:"
echo "-------------"

# Process each package
echo "$PACKAGES" | jq -r '.[].name' | while read -r pkg_name; do
    # Get versions for this package
    VERSIONS=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "https://api.github.com/users/gaineyllc/packages/$pkg_name/versions?per_page=100")
    
    # Calculate size for this package (sum of all versions)
    PKG_SIZE_BYTES=$(echo "$VERSIONS" | jq '[.[].package_container.metadata.container.tags[]?.size_bytes // 0] | add // 0')
    
    if [ "$PKG_SIZE_BYTES" -gt 0 ]; then
        PKG_SIZE_MB=$(echo "scale=2; $PKG_SIZE_BYTES / 1048576" | bc)
        echo "$pkg_name: ${PKG_SIZE_MB}MB"
    else
        echo "$pkg_name: 0MB (no container tags found)"
    fi
done

echo ""
echo "Note: API only shows container image sizes if tags are present."
echo "Total storage usage is the sum of all package versions."

# Check against free tier limit
FREE_TIER_LIMIT_GB=2
FREE_TIER_LIMIT_BYTES=$((FREE_TIER_LIMIT_GB * 1073741824))
THRESHOLD=$((FREE_TIER_LIMIT_BYTES * 80 / 100))  # 80%

if [ "$TOTAL_BYTES" -gt "$THRESHOLD" ]; then
    echo ""
    echo "⚠️ WARNING: Approaching free tier limit!"
    echo "Current usage: ${TOTAL_MB}MB"
    echo "Limit: ${FREE_TIER_LIMIT_GB}GB"
else
    echo ""
    echo "✅ Usage is within free tier limit."
fi

echo ""
echo "=== End of Report ==="
