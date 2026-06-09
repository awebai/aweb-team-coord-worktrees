# Claude Code adapter

Claude Code commonly reads `AGENTS.md` and/or `CLAUDE.md` from the workspace.
After creating an instance explicitly, link the chosen soul:

```bash
ln -sfn ../../souls/developer/AGENTS.md AGENTS.md
ln -sfn AGENTS.md CLAUDE.md
```

For a main-checkout coordinator, use `souls/coordinator/AGENTS.md` from the repo
root instead of the `../../` path.
