# Push Docker Images to GHCR

## Prerequisites
- GitHub Personal Access Token (PAT) with `read:packages` and `write:packages` scopes
- Docker installed locally
- `jq` installed for JSON parsing

## Setup

```bash
# Create a Personal Access Token (PAT)
# Go to: https://github.com/settings/tokens
# Generate new token with scopes:
#   - read:packages
#   - write:packages

export GITHUB_TOKEN="your-token-here"
export GITHUB_ACTOR="gaineyllc"
```

## Run the Push Script

```bash
# Navigate to the project directory
cd /home/gaineyllc/.openclaw/workspace/skymechanics-dev

# Run the push script
./scripts/push-images.sh
```

## What the Script Does

1. Authenticates to GHCR using your PAT
2. Builds all 5 Docker images:
   - auth-service
   - mechanics-service
   - jobs-service
   - analytics-service
   - gateway-service
3. Pushes each image to GHCR
4. Reports the size of each image
5. Calculates total storage usage
6. **Alerts if you're approaching the 2GB free tier limit**

## Storage Costs (Free Tier)

| Resource | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Package Storage | 2 GB | $0.50/GB/month |
| Data Transfer | 50 GB/month | Pay-per-use |

## Checking Storage Usage

You can check your current storage usage at:
https://github.com/settings/billing

Or via API:
```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/users/gaineyllc/settings/billing
```

## Manual Image Cleanup

If you need to free up space:

```bash
# List packages
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/users/gaineyllc/packages

# Delete old package versions
curl -X DELETE \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/users/gaineyllc/packages/auth-service/versions/{version_id}
```

## Monitoring Storage Usage

The push script includes automatic storage monitoring and alerts at 80% of the free tier limit (1.6GB). You'll see:

- ✅ Green: Usage below 1.6GB
- ⚠️ Yellow: Usage between 1.6GB and 2GB
- 🔴 Red: Usage over 2GB (may incur charges)
