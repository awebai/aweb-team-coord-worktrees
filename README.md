# Aweb team template: coordinator + developer/reviewer

A minimal Aweb team template with one long-lived coordinator and two repo-isolated coding agents:

- `coord` — coordinator role, home under `agents/home/coordinator/`, work points at the project repo root
- `dev` — developer role, home under `agents/home/developer/`, work points at `agents/worktrees/dev/`
- `review` — reviewer role, home under `agents/home/reviewer/`, work points at `agents/worktrees/review/`

This template is meant to be used with the `aw` CLI.

## Install `aw`

```bash
npm install -g @awebai/aw
aw version
```

## Bootstrap

Run from the root of the work repo where the agents should operate:

```bash
cd /path/to/your/project
aw team bootstrap https://github.com/awebai/aweb-team-coord-worktrees.git \
  --username <username>
```

Bootstrap creates an `agents/` directory inside the project repo. If `agents/` already exists, bootstrap fails before any side effects. Choose another name only when your repo already uses `agents/` for something else:

```bash
aw team bootstrap https://github.com/awebai/aweb-team-coord-worktrees.git \
  --username <username> \
  --agents-dir aweb-agents
```

If you want hosted onboarding prompts, omit `--username`. Default agent names from `team.yaml` are used automatically; pass `--ask-for-agent-names` only when you want to rename them interactively.

### Legacy compatibility

The old out-of-repo bootstrap mode still exists for compatibility. It is selected only when you pass `--work-directory` or `--work-repo-url`:

```bash
aw team bootstrap https://github.com/awebai/aweb-team-coord-worktrees.git \
  --username <username> \
  --work-directory /path/to/your/repo
```

Do not combine `--agents-dir` with legacy work flags.
Legacy mode is for old scripts and does not use this template's project-local `agents/home/` plus `agents/worktrees/` layout.

### Default in-repo output

After bootstrap you should have:

```text
your-project/
├─ agents/
│  ├─ docs/
│  ├─ roles/
│  ├─ team.yaml
│  ├─ home/
│  │  ├─ coordinator/
│  │  │  ├─ .aw/
│  │  │  ├─ AGENTS.md
│  │  │  └─ work -> ../../..
│  │  ├─ developer/
│  │  │  ├─ .aw/
│  │  │  ├─ AGENTS.md
│  │  │  └─ work -> ../../worktrees/dev
│  │  └─ reviewer/
│  │     ├─ .aw/
│  │     ├─ AGENTS.md
│  │     └─ work -> ../../worktrees/review
│  └─ worktrees/
│     ├─ dev/
│     └─ review/
├─ .gitignore               # bootstrap adds scoped ignores for .aw/ and worktrees/
└─ ...
```

Start the coordinator first:

```bash
cd agents/home/coordinator
claude
```

Then start the worktree agents when there is implementation or review work:

```bash
cd agents/home/developer
claude

cd agents/home/reviewer
claude
```

## Related skills and templates

If your coding agent supports aweb skills (for example through `@awebai/pi`), load these when useful:

- `aweb-bootstrap` — choose the right team source, work-directory/work-repo-url shape, worktree-agent policy, and rerun safety.
- `aweb-coordination` — day-to-day work loop, claims, handoffs, and shared state.
- `aweb-messaging` — mail/chat response policy and wake-up events.
- `aweb-team-membership` — invites, active team, certificates, hosted vs BYOT, and addressability.
- `aweb-identity` — identity, custody, `did:key`/`did:aw`, key rotation, and inbound mode.

Other maintained templates:

- [`aweb-team-dev-review`](https://github.com/awebai/aweb-team-dev-review) — minimal developer + reviewer pair.
- [`aweb-team-company-surfaces`](https://github.com/awebai/aweb-team-company-surfaces) — six persistent company-surface agents plus developer worktrees.

## Team model

The coordinator is the stable, long-lived team surface for intake and routing. The developer and reviewer are local worktree agents for code changes. Code edits should happen through each agent's `work/` symlink:

- `agents/home/developer/work` -> `agents/worktrees/dev`
- `agents/home/reviewer/work` -> `agents/worktrees/review`

The coordinator should:

1. clarify goals and acceptance criteria;
2. route implementation work to `dev`;
3. route review to `review`;
4. decide whether to request amendments, merge, or escalate.

## Structure

```text
team.yaml                    # roles and generated agent homes

docs/team.md                 # shared team operating instructions

roles/coordinator.md         # coordinator role playbook
roles/developer.md           # developer role playbook
roles/reviewer.md            # reviewer role playbook

home/coordinator/AGENTS.md   # coordinator home template
home/developer/AGENTS.md     # developer home template
home/reviewer/AGENTS.md      # reviewer home template
```

## Included team

| Surface | Default alias | Role name | Location |
|---|---:|---:|---|
| Coordinator | `coord` | `coordinator` | `agents/home/coordinator/` |
| Developer | `dev` | `developer` | `agents/home/developer/` |
| Reviewer | `review` | `reviewer` | `agents/home/reviewer/` |

## BYOT example

Bring Your Own Team (BYOT, including your own namespace/domain controller):

```bash
aw team bootstrap https://github.com/awebai/aweb-team-coord-worktrees.git \
  --aweb-url http://localhost:8000 \
  --registry http://localhost:8010 \
  --namespace example.com \
  --team coord-worktrees
```

If you do not yet have a local controller key for the namespace:

```bash
aw id namespace prepare-controller --domain example.com
```

## Real-time awakenings for mail/chat (recommended)

By default, agents do not automatically wake up when they receive aweb mail/chat. Without a wake-up path, ask them to check:

```bash
aw mail inbox
aw chat pending
```

Solutions:

- **Claude Code**: install the channel plugin from inside `claude`:
  ```
  /plugin marketplace add awebai/claude-plugins
  /plugin install aweb-channel@awebai-marketplace
  ```
  then restart with:
  ```bash
  claude --dangerously-load-development-channels plugin:aweb-channel@awebai-marketplace
  ```

- **Codex**:
  ```bash
  aw run codex
  ```

- **Pi**:
  ```bash
  pi install npm:@awebai/pi@latest
  ```

## License

This template is open source under the [MIT License](./LICENSE).
