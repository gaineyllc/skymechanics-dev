# SkyMechanics Backlog

## High Priority

## Medium Priority

## Low Priority / Future

### Sudoers Configuration (GB10)
- Issue: sudo command requires password despite NOPASSWD entry in `/etc/sudoers.d/skymechanics`
- Status: Need to fix sudoers file to give runner full systemctl access
- Impact: Runner service management (restart/start/stop) requires manual intervention

### GitHub Runner Token Management
- Issue: Runner registration requires a token with specific scopes
- Status: Fixed by generating registration token via `gh api` with correct token
- Future: Automate token generation and runner registration in setup scripts

## Completed

### GitHub Runner Setup (2026-04-21 17:18)
- Runner successfully registered as `promaxgb10-495f`
- Runner is online and listening for jobs
- Service file configured at `/home/gaineyllc/github-runner/github-runner.service`
- Runner running in background

### CI/CD Pipeline Configuration
- Workflow: `.github/workflows/cicd.yml` configured
- 10 microservices ready for Docker build and push to GHCR
- Kubernetes deployment steps ready (requires KUBECONFIG secret)

## Notes

- Runner is currently running in background mode
- Service file exists but requires sudoers fix to manage via systemctl
- Token needs to be rotated periodically or automated via GitHub App
