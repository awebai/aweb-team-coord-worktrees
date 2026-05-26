# Aweb team template: coordinator + developer/reviewer worktrees

A minimal Aweb team template with one long-lived coordinator workspace and two repo-isolated worktree agents:

- `coord` — coordinator role, persistent responsibility workspace under `agents/coordinator/`
- `dev` — developer role, generated git worktree under `worktrees/<repo>-dev/`
- `review` — reviewer role, generated git worktree under `worktrees/<repo>-review/`

This template is meant to be used with the `aw` CLI.

## Install `aw`

```bash
npm install -g @awebai/aw
aw version
```

## Bootstrap

Run from a directory that is **not already inside a git repo/worktree**. For remote templates, `aw team bootstrap` refuses to clone into an existing git worktree unless you pass `--template-cache-dir`.

This template declares `worktrees:` in `team.yaml`, so the work directory must be a git repo. Pass exactly one of:

- `--work-directory <path>` — use an existing local git repo
- `--work-repo-url <url-or-local-path>` — clone a repo into `./worktrees/<derived-name>/` inside the template checkout

### Recommended: clone the work repo into worktrees/

```bash
aw team bootstrap https://github.com/awebai/aweb-team-coord-worktrees.git \
  --username <username> \
  --work-repo-url https://github.com/<org>/<repo>.git
```

### Alternative: use an existing local work repo

```bash
aw team bootstrap https://github.com/awebai/aweb-team-coord-worktrees.git \
  --username <username> \
  --work-directory /path/to/your/repo
```

If you want hosted onboarding prompts, omit `--username`.
Default agent names from `team.yaml` are used automatically; pass `--ask-for-agent-names` only when you want to rename them interactively.

After bootstrap you should have:

```text
aweb-team-coord-worktrees/
├─ agents/
│  └─ coordinator/          # long-lived coordinator workspace
│     ├─ .aw/
│     ├─ AGENTS.md
│     └─ work -> ../worktrees/<repo>/ or /path/to/your/repo
└─ worktrees/
   ├─ <repo>/               # only when --work-repo-url was used
   ├─ <repo>-dev/           # developer worktree agent
   │  └─ .aw/
   └─ <repo>-review/        # reviewer worktree agent
      └─ .aw/
```

Start the coordinator first:

```bash
cd aweb-team-coord-worktrees/agents/coordinator
claude
```

Then start the worktree agents when there is implementation or review work:

```bash
cd ../../worktrees/<repo>-dev
claude

cd ../<repo>-review
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

The coordinator is the stable, long-lived team surface for intake and routing. The developer and reviewer are local worktree agents for code changes. Code edits should happen in `worktrees/<repo>-dev/`; independent review should happen from `worktrees/<repo>-review/`.

The coordinator should:

1. clarify goals and acceptance criteria;
2. route implementation work to `dev`;
3. route review to `review`;
4. decide whether to request amendments, merge, or escalate.

## Structure

```text
team.yaml                    # roles, one coordinator agent, two worktree agents

docs/team.md                 # shared team operating instructions

roles/coordinator.md         # coordinator role playbook
roles/developer.md           # developer role playbook
roles/reviewer.md            # reviewer role playbook

agents/coordinator/AGENTS.md # coordinator workspace context
worktrees/                   # generated git worktrees; not template source
```

## Included team

| Surface | Default alias | Role name | Location |
|---|---:|---:|---|
| Coordinator | `coord` | `coordinator` | `agents/coordinator/` |
| Developer worktree | `dev` | `developer` | `worktrees/<repo>-dev/` |
| Reviewer worktree | `review` | `reviewer` | `worktrees/<repo>-review/` |

## BYOT example

Bring Your Own Team (BYOT, including your own namespace/domain controller):

```bash
aw team bootstrap https://github.com/awebai/aweb-team-coord-worktrees.git \
  --aweb-url http://localhost:8000 \
  --registry http://localhost:8010 \
  --namespace example.com \
  --team coord-worktrees \
  --work-directory /path/to/your/repo
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
