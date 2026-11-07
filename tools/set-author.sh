#!/usr/bin/env bash
# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Linux counterpart of tools/set-author.ps1; sets the repository-local Git author for the active team member.
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "Usage: tools/set-author.sh ibrahim|omer" >&2
  exit 2
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[ -d "$repo_root/.git" ] || { echo "Not a git repository: $repo_root" >&2; exit 1; }

case "$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')" in
  ibrahim) name="Ibrahim Temur";   email="ibrahimtemur847@gmail.com"; no="231805033" ;;
  omer)    name="Omer Faruk Kuş"; email="kusomer889@gmail.com";       no="231805026" ;;
  *) echo "Unknown author '$1' (use ibrahim or omer)" >&2; exit 2 ;;
esac

git -C "$repo_root" config --local user.name "$name"
git -C "$repo_root" config --local user.email "$email"
echo "Repository-local Git author set to: $(git -C "$repo_root" config --local --get user.name) ($no) <$(git -C "$repo_root" config --local --get user.email)>"
