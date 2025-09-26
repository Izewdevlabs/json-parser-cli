#!/usr/bin/env bash
set -euo pipefail

# --- CONFIG --- #
GITHUB_USER="your-username"   # 🔁 replace with your GitHub username/org
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
