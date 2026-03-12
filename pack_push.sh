#!/usr/bin/env bash
set -euo pipefail

# Usage: ./pack_push.sh "message de commit"
# Exemple: ./pack_push.sh "Add OCR pipeline"

COMMIT_MSG="${1:-}"

if [[ -z "$COMMIT_MSG" ]]; then
  echo "Usage: ./pack_push.sh \"message de commit\""
  exit 1
fi

# Verifie qu'on est dans un repo git
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Erreur: ce dossier n'est pas un repository git."
  exit 1
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD)"

echo "[1/4] Ajout des fichiers modifies..."
git add -A

echo "[2/4] Verification des changements..."
if git diff --cached --quiet; then
  echo "Aucun changement a commit."
  exit 0
fi

echo "[3/4] Commit..."
git commit -m "$COMMIT_MSG"

echo "[4/4] Push sur origin/$BRANCH..."
git push origin "$BRANCH"

echo "Termine: commit et push effectues sur $BRANCH"
