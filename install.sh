#!/usr/bin/env bash
# dotfiles bootstrap — run from inside ~/dotfiles
# usage: ./install.sh
set -e
PACKAGES=()
for dir in */; do
    dir="${dir%/}"
    [[ "$dir" == ".git" ]] && continue
    PACKAGES+=("$dir")
done
DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "==> dotfiles bootstrap starting from $DOTFILES_DIR"
# 1. make sure stow is installed
if ! command -v stow &>/dev/null; then
    echo "==> stow not found, installing..."
    sudo pacman -S --needed --noconfirm stow
fi
cd "$DOTFILES_DIR"
# 2. for each package, check for pre-existing real files/dirs that would
#    block stow, and warn instead of silently deleting anything
for pkg in "${PACKAGES[@]}"; do
    echo "==> checking $pkg"
    # dry run to catch conflicts before touching anything
    if ! stow -n -v "$pkg" 2>/tmp/stow_conflict_$pkg; then
        echo "    CONFLICT for $pkg — existing files found:"
        cat /tmp/stow_conflict_$pkg
        echo "    Skipping $pkg. Resolve manually (back up + remove the"
        echo "    conflicting real files/dirs), then run: stow $pkg"
        rm -f /tmp/stow_conflict_$pkg
        continue
    fi
    rm -f /tmp/stow_conflict_$pkg
    stow "$pkg"
    echo "    $pkg stowed OK"
done
echo "==> done. Verify symlinks with: ls -la ~/.config | grep '\->'"
