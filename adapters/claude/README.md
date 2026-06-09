# Claude Code adapter

Claude Code reads `CLAUDE.md` (and `AGENTS.md`) from the workspace and loads
skills from `.claude/skills`.

At the repo root, after installing the blueprint resources:

```bash
ln -sfn .agents/skills .claude/skills
```

In each instance home, after wiring the body:

```bash
ln -sfn AGENTS.md CLAUDE.md
```

For message wake-up, install the aweb channel plugin once per machine:

```text
/plugin marketplace add awebai/claude-plugins
/plugin install aweb-channel@awebai-marketplace
```

Launch from the instance home: `cd agents/instances/<name> && claude`.

Do not overwrite a project-root `AGENTS.md` or `CLAUDE.md` just to start
Claude Code; instances have their own homes.
