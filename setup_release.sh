#!/usr/bin/env bash
set -euo pipefail

# --- CONFIG DETECTION --- #
# Try to get GitHub user from global config
GITHUB_USER=$(git config --get github.user || true)

if [[ -z "$GITHUB_USER" ]]; then
  # fallback: try git user.name
  GITHUB_USER=$(git config --get user.name || true)
fi

if [[ -z "$GITHUB_USER" ]]; then
  echo "❌ Could not auto-detect GitHub username."
  echo "👉 Please set it with: git config --global github.user <username>"
  exit 1
fi

REPO="json-parser-cli"

# --- SCRIPT --- #
# Extract version from pyproject.toml
VERSION=$(grep '^version' pyproject.toml | cut -d '"' -f2)

echo "📦 Preparing release v$VERSION for $GITHUB_USER/$REPO"

git init
git add .
git commit -m "chore: initial commit v$VERSION" || echo "✅ commit already exists"

git branch -M main
git remote add origin git@github.com:$GITHUB_USER/$REPO.git 2>/dev/null || echo "🔗 remote already exists"

git push -u origin main

git tag "v$VERSION" || echo "🏷️ tag already exists"
git push origin "v$VERSION"

echo "🎉 Done! Release pipeline will run on GitHub Actions."
