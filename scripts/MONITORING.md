# Storage Monitoring Guide

## Free Tier Limits

| Resource | Free Tier | Alert Threshold | Paid Tier |
|----------|-----------|-----------------|-----------|
| Package Storage | 2 GB | 1.6 GB (80%) | $0.50/GB/month |
| Data Transfer | 50 GB/month | 40 GB (80%) | Pay-per-use |

## Monitoring Commands

### Check Current Storage Usage

```bash
# Must have GITHUB_TOKEN set
export GITHUB_TOKEN="your-token-here"

# Run the storage check script
./scripts/check-storage.sh
```

### Push Images with Automatic Monitoring

```bash
# Must have GITHUB_TOKEN set
export GITHUB_TOKEN="your-token-here"

# Run the push script - it will alert if approaching limits
./scripts/push-images.sh
```

## Storage Alerts

### When You Get Alerts

| Alert Level | Storage Used | Action Required |
|-------------|--------------|-----------------|
| ✅ Green | < 1.6 GB | None |
| ⚠️ Yellow | 1.6 - 1.9 GB | Review packages, consider cleanup |
| 🔴 Red | > 1.9 GB | Immediate cleanup required |

### Cleanup Options

1. **Delete old package versions**
   ```bash
   curl -X DELETE \
     -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/users/gaineyllc/packages/{package_name}/versions/{version_id}
   ```

2. **Delete unused packages**
   ```bash
   curl -X DELETE \
     -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/users/gaineyllc/packages/{package_name}
   ```

3. **Use GitHub UI**
   - Go to https://github.com/settings/packages
   - Select packages to delete
   - Click "Delete" button

## Cost Estimation

If you exceed the free tier:

| Usage Level | Monthly Cost |
|-------------|--------------|
| 2-3 GB | $0.50 |
| 3-5 GB | $1.00-2.50 |
| 5-10 GB | $2.50-5.00 |

For a small project like SkyMechanics (5 services), typical usage will be:
- Initial push: ~1 GB
- Monthly updates: +500 MB
- **Total**: ~1.5 GB (within free tier)

## GitHub Billing Page

View your actual usage at:
https://github.com/settings/billing

This shows:
- Total storage used
- Data transfer usage
- Actions minutes used
- Estimated charges

## Daily Monitoring Routine

Add this to your shell profile for quick checks:

```bash
# Add to ~/.bashrc or ~/.zshrc
ghcr-status() {
    export GITHUB_TOKEN="your-token-here"
    ./scripts/check-storage.sh
}
```

Then run `ghcr-status` anytime to check storage.
