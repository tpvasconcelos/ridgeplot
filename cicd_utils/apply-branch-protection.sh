#!/usr/bin/env bash

# Apply the repository's required-status-checks configuration to main
#
# The status checks that must pass before merging into main are kept as
# config-as-code in .github/required-status-checks.json (the single
# source of truth; GitHub's branch protection settings UI is just a
# mirror of it). This script pushes that configuration to GitHub. It
# shows the current and desired configurations and asks for
# confirmation before applying (pass --yes to skip the prompt).
#
# Notes on the configuration itself:
# * "checks" should only ever contain stable, first-party contexts. In
#   particular, the "All CI checks passed" gate job in ci.yml covers
#   the whole test matrix, so adding/dropping Python versions never
#   requires updating this list. External services (codecov,
#   pre-commit.ci, Read the Docs, etc.) are advisory by design: they
#   stay visible on PRs, but merges don't depend on their uptime.
# * "strict" means PR branches must be up to date with main before
#   merging (bot PRs are kept up to date automatically by the heal job
#   in .github/workflows/bot-pr-automation.yml).
#
# Usage: ./cicd_utils/apply-branch-protection.sh [--yes]
#
# Requirements:
# * GitHub CLI (gh) must be installed and authenticated.
# * jq must be installed for JSON parsing.
# * The authenticated user must have admin access to the repository
#   (branch protection can only be read and written by admins).
# * The script should be run from the root of the repository.

set -euo pipefail

CONFIG_FILE=".github/required-status-checks.json"
BRANCH="main"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "Error: Config file not found at $CONFIG_FILE (run this script from the repo root)"
    exit 1
fi

if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed"
    exit 1
fi

repo=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
endpoint="repos/${repo}/branches/${BRANCH}/protection/required_status_checks"
normalize='{strict: .strict, checks: [.checks[] | {context: .context}]}'

echo "🔍 Current configuration (${repo}, branch: ${BRANCH}):"
if current=$(gh api "$endpoint" --jq "$normalize" 2>/dev/null); then
    echo "$current" | jq .
else
    current=""
    echo "(no required status checks are currently configured)"
fi
echo

echo "📄 Desired configuration (from ${CONFIG_FILE}):"
desired=$(jq "$normalize" "$CONFIG_FILE")
echo "$desired" | jq .
echo

if [[ -n "$current" && "$(echo "$current" | jq -S .)" == "$(echo "$desired" | jq -S .)" ]]; then
    echo "✅ Branch protection is already in sync with ${CONFIG_FILE}; nothing to do."
    exit 0
fi

if [[ "${1:-}" != "--yes" ]]; then
    read -r -p "Apply the desired configuration? [y/N] " answer || answer=""
    if [[ "$answer" != "y" && "$answer" != "Y" ]]; then
        echo "Aborted."
        exit 1
    fi
fi

gh api -X PATCH "$endpoint" --input "$CONFIG_FILE" > /dev/null
echo "🚀 Applied. New configuration:"
gh api "$endpoint" --jq "$normalize" | jq .
