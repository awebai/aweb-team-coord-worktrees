#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: $0 /path/to/project" >&2
  exit 2
fi

src="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dest="$1"

if [ ! -d "$dest" ]; then
  echo "target project does not exist: $dest" >&2
  exit 1
fi

copy_dir() {
  local from="$1" to="$2"
  if [ -e "$to" ]; then
    echo "refusing to overwrite existing path: $to" >&2
    exit 1
  fi
  cp -R "$from" "$to"
}

copy_file() {
  local from="$1" to="$2"
  if [ -e "$to" ]; then
    echo "refusing to overwrite existing path: $to" >&2
    exit 1
  fi
  cp "$from" "$to"
}

mkdir -p "$dest/agents/souls" "$dest/agents/roles" "$dest/agents/docs" \
  "$dest/.agents/skills" "$dest/.agents/bin"

for soul in coordinator developer reviewer; do
  copy_dir "$src/resources/souls/$soul" "$dest/agents/souls/$soul"
done

for skill in spawn-instance get-code-reviewed self-maintenance; do
  copy_dir "$src/skills/$skill" "$dest/.agents/skills/$skill"
done

for role_file in "$src"/resources/roles/*.md; do
  copy_file "$role_file" "$dest/agents/roles/$(basename "$role_file")"
done

copy_file "$src/resources/instructions.md" "$dest/agents/instructions.md"
copy_file "$src/resources/docs/team-architecture.md" "$dest/agents/docs/team-architecture.md"
copy_file "$src/resources/bin/launch-session.sh" "$dest/.agents/bin/launch-session.sh"
chmod +x "$dest/.agents/bin/launch-session.sh"
"$src/scripts/build-roles-bundle.py" > "$dest/agents/roles-bundle.json"

cat <<EOF
Installed the coordinator-with-dev-review team resources into $dest

Next steps:
  1. cd $dest
  2. Keep instances out of git:
       printf '/agents/instances/\n' >> .gitignore
  3. For Claude Code, link the skills dir:
       ln -sfn .agents/skills .claude/skills
  4. Review and commit the team resources:
       git add agents .agents .claude .gitignore
       git commit -m "Add coordinator/developer/reviewer team from blueprint"
  5. Create and connect the first instance (usually coordinator):
       see $src/examples/deploy.md steps 3-4
  6. From the connected instance home, publish shared context:
       aw instructions set --body-file ../../instructions.md
       aw roles set --bundle-file ../../roles-bundle.json
EOF
