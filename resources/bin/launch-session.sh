#!/usr/bin/env bash
# Launch an agent session for an instance home, optionally in tmux.
#
# One-time setup per machine for message wake-up:
#   Claude Code — /plugin marketplace add awebai/claude-plugins
#                 /plugin install aweb-channel@awebai-marketplace
#   Pi          — pi install npm:@awebai/pi@latest
set -euo pipefail

runtime=claude; use_tmux=0; dir=""
for a in "$@"; do
  case "$a" in
    --claude) runtime=claude ;;
    --pi)     runtime=pi ;;
    --tmux)   use_tmux=1 ;;
    *)        dir="$a" ;;
  esac
done

if [ -z "$dir" ]; then
  echo "usage: launch-session.sh <instance-home> [--claude|--pi] [--tmux]" >&2
  exit 2
fi
[ -d "$dir" ] || { echo "launch-session: no such directory: $dir" >&2; exit 1; }
dir="$(cd "$dir" && pwd)"

case "$runtime" in
  claude) cmd='claude' ;;
  pi)     cmd='pi' ;;
esac

name="$(basename "$dir")"
if [ "$use_tmux" = 1 ]; then
  command -v tmux >/dev/null 2>&1 || { echo "launch-session: tmux not installed." >&2; exit 1; }
  REPO="$(cd "$(git -C "$dir" rev-parse --git-common-dir)" && cd .. && pwd)"
  sess="$(basename "$REPO")"
  tmux has-session -t "$sess" 2>/dev/null || tmux new-session -d -s "$sess" -n team
  # Size windows to the LATEST active client so a stray 1-row pseudo-terminal
  # cannot shrink the session into a garbled render.
  tmux set-option -g window-size latest 2>/dev/null || true
  tmux set-option -g aggressive-resize on 2>/dev/null || true
  tmux new-window -t "$sess" -n "$name" -c "$dir" "$cmd"
  echo "Launched $runtime in tmux: session '$sess', window '$name'."
  echo "Attach with:  tmux attach -t $sess"
else
  echo "To launch a $runtime session, run:"
  echo "  cd \"$dir\" && $cmd"
fi
