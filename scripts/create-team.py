#!/usr/bin/env python3
"""Create a team from this blueprint in one go.

Reads the blueprint (manifest + souls), asks how many instances of each soul
you want, connects them all to aweb, and prints the launch commands.

Team source, in order of precedence:
  - AWEB_API_KEY in the environment (joins/uses that hosted team);
  - --invite-token (joins the inviting team);
  - --username (creates a hosted account; prompted for if interactive).

Every identity is created with explicit aw commands, shown as they run.
Nothing is deleted on failure: the script stops, reports exactly what was
created, and points at the retire-instance skill for cleanup.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

BLUEPRINT = Path(__file__).resolve().parents[1]
# Every skill the blueprint ships travels into the target, except the
# one-shot create-team procedure itself.
SKILLS_TO_INSTALL = sorted(
    p.name for p in (BLUEPRINT / "skills").iterdir()
    if p.is_dir() and p.name != "create-team"
)


def fail(msg: str) -> None:
    print(f"\nerror: {msg}", file=sys.stderr)
    sys.exit(1)


def run(cmd: list[str], cwd: Path, *, env: dict | None = None) -> str:
    print(f"  $ {' '.join(cmd)}    (in {cwd})")
    proc = subprocess.run(
        cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=120
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"command failed: {' '.join(cmd)}\n{proc.stdout}\n{proc.stderr}"
        )
    return proc.stdout


def read_souls() -> list[dict]:
    souls = []
    for soul_dir in sorted((BLUEPRINT / "resources" / "souls").iterdir()):
        meta_file = soul_dir / "soul.yaml"
        if not soul_dir.is_dir() or not meta_file.exists():
            continue
        meta = {"role": soul_dir.name, "work": "main", "runtime": "claude"}
        for line in meta_file.read_text().splitlines():
            m = re.match(r"^(role|work|runtime):\s*(\S+)", line)
            if m:
                meta[m.group(1)] = m.group(2)
        meta["name"] = soul_dir.name
        souls.append(meta)
    if not souls:
        fail(f"no souls found under {BLUEPRINT}/resources/souls")
    return souls


def ask_counts(souls: list[dict], counts_arg: str | None, assume_yes: bool) -> dict[str, int]:
    given: dict[str, int] = {}
    if counts_arg:
        for part in counts_arg.split(","):
            name, _, n = part.partition("=")
            if name.strip() not in {s["name"] for s in souls}:
                fail(f"unknown soul in --counts: {name.strip()}")
            given[name.strip()] = int(n)
    counts: dict[str, int] = {}
    for soul in souls:
        default = 1
        if soul["name"] in given:
            counts[soul["name"]] = given[soul["name"]]
        elif assume_yes or not sys.stdin.isatty():
            counts[soul["name"]] = default
        else:
            raw = input(
                f"How many '{soul['name']}' instances? (work: {soul['work']}, runtime: {soul['runtime']}) [{default}]: "
            ).strip()
            counts[soul["name"]] = int(raw) if raw else default
    if sum(counts.values()) == 0:
        fail("nothing to create: all counts are zero")
    return counts


def plan_instances(souls: list[dict], counts: dict[str, int]) -> list[dict]:
    instances = []
    for soul in souls:
        n = counts.get(soul["name"], 0)
        for i in range(n):
            alias = soul["name"] if i == 0 else f"{soul['name']}-{i + 1}"
            instances.append({**soul, "alias": alias})
    # Anchor first: prefer a standing (work: main) instance.
    instances.sort(key=lambda x: 0 if x["work"] == "main" else 1)
    return instances


def install_resources(target: Path) -> None:
    if (target / "agents" / "souls").exists():
        print("  agents/souls already present in target; skipping resource copy")
        return
    for d in ("agents/souls", "agents/roles", "agents/docs", ".agents/skills"):
        (target / d).mkdir(parents=True, exist_ok=True)
    for soul_dir in sorted((BLUEPRINT / "resources" / "souls").iterdir()):
        if soul_dir.is_dir():
            shutil.copytree(soul_dir, target / "agents" / "souls" / soul_dir.name)
    for role_file in sorted((BLUEPRINT / "resources" / "roles").glob("*.md")):
        shutil.copy(role_file, target / "agents" / "roles" / role_file.name)
    shutil.copy(BLUEPRINT / "resources" / "instructions.md", target / "agents" / "instructions.md")
    arch = BLUEPRINT / "resources" / "docs" / "team-architecture.md"
    if arch.exists():
        shutil.copy(arch, target / "agents" / "docs" / "team-architecture.md")
    for skill in SKILLS_TO_INSTALL:
        src = BLUEPRINT / "skills" / skill
        if src.exists():
            shutil.copytree(src, target / ".agents" / "skills" / skill)
    bin_dir = BLUEPRINT / "resources" / "bin"
    if bin_dir.is_dir():
        (target / ".agents" / "bin").mkdir(parents=True, exist_ok=True)
        for helper in bin_dir.iterdir():
            dest = target / ".agents" / "bin" / helper.name
            shutil.copy(helper, dest)
            dest.chmod(0o755)
    bundle = subprocess.run(
        [str(BLUEPRINT / "scripts" / "build-roles-bundle.py")],
        capture_output=True, text=True, check=True,
    ).stdout
    (target / "agents" / "roles-bundle.json").write_text(bundle)
    claude_skills = target / ".claude" / "skills"
    if not claude_skills.exists():
        claude_skills.parent.mkdir(exist_ok=True)
        claude_skills.symlink_to("../.agents/skills")
    gitignore = target / ".gitignore"
    line = "/agents/instances/"
    existing = gitignore.read_text() if gitignore.exists() else ""
    if line not in existing:
        with gitignore.open("a") as f:
            if existing and not existing.endswith("\n"):
                f.write("\n")
            f.write(line + "\n")
    print("  installed agents/ + .agents/ resources")


def make_home(target: Path, inst: dict) -> Path:
    home = target / "agents" / "instances" / inst["alias"]
    if (home / ".aw").exists():
        raise RuntimeError(f"{home} already has an identity; retire it first or pick another alias")
    home.mkdir(parents=True, exist_ok=True)
    (home / "AGENTS.md").unlink(missing_ok=True)
    (home / "AGENTS.md").symlink_to(f"../../souls/{inst['name']}/AGENTS.md")
    if inst["runtime"] == "claude":
        (home / "CLAUDE.md").unlink(missing_ok=True)
        (home / "CLAUDE.md").symlink_to("AGENTS.md")
    return home


def make_work(target: Path, inst: dict, home: Path, created: list[str]) -> None:
    if inst["work"] == "worktree":
        run(["git", "worktree", "add", str(home / "work"), "-b", inst["alias"]], cwd=target)
        created.append(f"worktree+branch {inst['alias']}")
    else:
        work = home / "work"
        if not work.exists():
            work.symlink_to("../../..")


def launch_cmd(inst: dict) -> str:
    runtime = {"claude": "claude", "pi": "pi", "codex": "codex"}.get(inst["runtime"], inst["runtime"])
    return f"cd agents/instances/{inst['alias']} && {runtime}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="path to the repo where the team should live")
    ap.add_argument("--counts", help="comma list, e.g. coordinator=1,developer=2,reviewer=0")
    ap.add_argument("--username", help="hosted username to create (when no AWEB_API_KEY)")
    ap.add_argument("--invite-token", help="join an existing team via invite token")
    ap.add_argument("--aweb-url", help="override AWEB_URL")
    ap.add_argument("--yes", action="store_true", help="accept defaults, no prompts")
    ap.add_argument("--dry-run", action="store_true", help="print the plan and exit")
    publish = ap.add_mutually_exclusive_group()
    publish.add_argument("--publish", action="store_true", help="publish instructions/roles even when joining an existing team")
    publish.add_argument("--no-publish", action="store_true", help="never publish instructions/roles")
    args = ap.parse_args()

    target = Path(args.target).resolve()
    if not target.is_dir():
        fail(f"target does not exist: {target}")
    if not (target / ".git").exists():
        fail(f"target is not a git repo: {target} (needed for developer worktrees)")
    if not shutil.which("aw"):
        fail("aw CLI not found on PATH (npm install -g @awebai/aw)")

    souls = read_souls()
    counts = ask_counts(souls, args.counts, args.yes)
    instances = plan_instances(souls, counts)

    api_key = os.environ.get("AWEB_API_KEY", "").strip()
    source = "api-key" if api_key else "invite-token" if args.invite_token else "username"
    username = args.username
    if source == "username" and not username:
        if args.yes or not sys.stdin.isatty():
            fail("no AWEB_API_KEY in env and no --username/--invite-token given")
        username = input("Hosted username to create: ").strip()
        if not username:
            fail("a username is required without AWEB_API_KEY")

    print(f"\nPlan: {len(instances)} instance(s) in {target}")
    for inst in instances:
        print(f"  - {inst['alias']:24} soul={inst['name']:12} work={inst['work']:8} runtime={inst['runtime']}")
    print(f"  team source: {source}")
    if args.dry_run:
        return
    if not args.yes and sys.stdin.isatty():
        if input("Proceed? [Y/n]: ").strip().lower() not in ("", "y", "yes"):
            sys.exit(0)

    env = os.environ.copy()
    if args.aweb_url:
        env["AWEB_URL"] = args.aweb_url

    created: list[str] = []
    try:
        install_resources(target)

        anchor, rest = instances[0], instances[1:]
        print(f"\n[1/{len(instances)}] anchor: {anchor['alias']}")
        home = make_home(target, anchor)
        created.append(f"instance {anchor['alias']}")
        init_base = ["aw", "init", "--alias", anchor["alias"], "--do-not-touch-agents-md"]
        if source == "invite-token":
            run(["aw", "id", "team", "accept-invite", args.invite_token, "--alias", anchor["alias"]], cwd=home, env=env)
            run(init_base, cwd=home, env=env)
        elif source == "api-key":
            run(init_base, cwd=home, env=env)
        else:
            run(init_base + ["--username", username], cwd=home, env=env)
        make_work(target, anchor, home, created)

        # A fresh hosted team gets the blueprint's shared context. Joining an
        # existing team must not silently overwrite what that team already
        # published — require --publish (or an interactive yes) there.
        do_publish = not args.no_publish and (
            source == "username"
            or args.publish
            or (
                not args.yes
                and sys.stdin.isatty()
                and input(
                    "Publish this blueprint's instructions/roles to the team? "
                    "This OVERWRITES whatever the team already has. [y/N]: "
                ).strip().lower() in ("y", "yes")
            )
        )
        if do_publish:
            print("\npublishing shared team context")
            run(["aw", "instructions", "set", "--body-file", "../../instructions.md"], cwd=home, env=env)
            run(["aw", "roles", "set", "--bundle-file", "../../roles-bundle.json"], cwd=home, env=env)
        else:
            print("\nskipping instructions/roles publish (existing team; use --publish to push the blueprint's)")

        anchor_home = home
        for i, inst in enumerate(rest, start=2):
            print(f"\n[{i}/{len(instances)}] {inst['alias']}")
            out = run(["aw", "id", "team", "invite"], cwd=anchor_home, env=env)
            m = re.search(r"^Token:\s*(\S+)", out, re.M)
            if not m:
                raise RuntimeError(f"could not parse invite token from:\n{out}")
            home = make_home(target, inst)
            created.append(f"instance {inst['alias']}")
            run(["aw", "id", "team", "accept-invite", m.group(1), "--alias", inst["alias"]], cwd=home, env=env)
            run(["aw", "init", "--alias", inst["alias"], "--do-not-touch-agents-md"], cwd=home, env=env)
            make_work(target, inst, home, created)
    except Exception as exc:  # noqa: BLE001
        print(f"\nFAILED: {exc}", file=sys.stderr)
        if created:
            print("\nCreated before the failure (NOT removed automatically):", file=sys.stderr)
            for c in created:
                print(f"  - {c}", file=sys.stderr)
            print(
                "Homes containing .aw hold real identities. Clean up with the\n"
                "retire-instance skill (.agents/skills/retire-instance/), or rerun\n"
                "after fixing the cause; existing identities are never overwritten.",
                file=sys.stderr,
            )
        sys.exit(1)

    print("\nDone. Review and commit the team resources:")
    print("  git add agents .agents .claude .gitignore && git commit -m 'Add team from blueprint'")
    print("\nLaunch your team (one terminal each):")
    for inst in instances:
        print(f"  {launch_cmd(inst)}")


if __name__ == "__main__":
    main()
