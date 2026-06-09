#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: $0 /path/to/project" >&2
  exit 2
fi

src="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dest="$1"
pattern="coordinator-with-dev-review"
out="$dest/team-operating-patterns/$pattern"

if [ ! -d "$dest" ]; then
  echo "target project does not exist: $dest" >&2
  exit 1
fi

mkdir -p "$dest/souls" "$dest/.agents/skills" "$out"

copy_dir() {
  local from="$1" to="$2"
  if [ -e "$to" ]; then
    echo "refusing to overwrite existing path: $to" >&2
    exit 1
  fi
  cp -R "$from" "$to"
}

for soul in coordinator developer reviewer; do
  copy_dir "$src/resources/souls/$soul" "$dest/souls/$soul"
done

for skill in spawn-instance self-maintenance; do
  copy_dir "$src/skills/$skill" "$dest/.agents/skills/$skill"
done

cp "$src/resources/instructions.md" "$out/instructions.md"
cp "$src/resource-pack.yaml" "$out/resource-pack.yaml"
"$src/scripts/build-roles-bundle.py" > "$out/roles-bundle.json"

cat <<EOF
Installed $pattern into $dest

Next steps from the project root:
  aw instructions set --body-file team-operating-patterns/$pattern/instructions.md
  aw roles set --bundle-file team-operating-patterns/$pattern/roles-bundle.json

Then create concrete instances explicitly when needed. See:
  $src/examples/create-instance.md
EOF
