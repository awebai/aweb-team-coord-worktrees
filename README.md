# Aweb team template: coordinator + developer/reviewer

A minimal Aweb team template with one long-lived coordinator and two repo-isolated coding agents:

- `coordinator` — local coordinator responsibility, home under `agents/home/coordinator/`, work points at the project repo root
- `developer` — local developer responsibility, home under `agents/home/developer/`, work points at `agents/worktrees/developer/`
- `reviewer` — local reviewer responsibility, home under `agents/home/reviewer/`, work points at `agents/worktrees/reviewer/`

This template is source input for the `aw agents` CLI. It does not contain final per-human aliases, DIDs, global addresses, certificates, or private keys. Those are generated per human under ignored `.aw/` state.

## Install `aw`

```bash
npm install -g @awebai/aw
aw version
```

## Bootstrap

Run from the root of the work repo where the agents should operate:

```bash
cd /path/to/your/project
aw agents bootstrap https://github.com/awebai/aweb-team-coord-worktrees.git \
  --username <username> \
  --identity-prefix <your-name>
```

Bootstrap creates an `agents/` directory inside the project repo. If `agents/` already exists, bootstrap fails before any side effects. Choose another name only when your repo already uses `agents/` for something else:

```bash
aw agents bootstrap https://github.com/awebai/aweb-team-coord-worktrees.git \
  --username <username> \
  --identity-prefix <your-name> \
  --agents-dir aweb-agents
```

If you want hosted onboarding prompts, omit `--username`. The naming policy in `team.yaml` allocates per-human aliases automatically. Use `--identity-prefix` or set `AWEB_IDENTITY_PREFIX` so each human gets distinct team aliases and any global agents you add later get unique public names.

Preview first:

```bash
aw agents bootstrap https://github.com/awebai/aweb-team-coord-worktrees.git \
  --username <username> \
  --identity-prefix <your-name> \
  --dry-run
```

### Legacy compatibility

The old out-of-repo bootstrap mode still exists for compatibility. It is selected only when you pass `--work-directory` or `--work-repo-url`:

```bash
aw agents bootstrap https://github.com/awebai/aweb-team-coord-worktrees.git \
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
│  │  │  └─ work -> ../../worktrees/developer
│  │  └─ reviewer/
│  │     ├─ .aw/
│  │     ├─ AGENTS.md
│  │     └─ work -> ../../worktrees/reviewer
│  └─ worktrees/
│     ├─ developer/
│     └─ reviewer/
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

- `aweb-bootstrap` — choose the right team source, repo-local layout, worktree-agent policy, and rerun safety.
- `aweb-coordination` — day-to-day work loop, claims, handoffs, and shared state.
- `aweb-messaging` — mail/chat response policy and wake-up events.
- `aweb-team-membership` — invites, active team, certificates, hosted vs BYOT, and addressability.
- `aweb-identity` — identity, custody, `did:key`/`did:aw`, key rotation, and inbound mode.

Other maintained templates:

- [`aweb-team-company-surfaces`](https://github.com/awebai/aweb-team-company-surfaces) — six persistent company-surface agents plus a developer worktree.

## Team model

The coordinator is the stable, long-lived team surface for intake and routing. The developer and reviewer are local worktree agents for code changes. Code edits should happen through each agent's `work/` symlink:

- `agents/home/developer/work` -> `agents/worktrees/developer`
- `agents/home/reviewer/work` -> `agents/worktrees/reviewer`

The coordinator should:

1. clarify goals and acceptance criteria;
2. route implementation work to the allocated alias for the `developer` responsibility;
3. route review to the allocated alias for the `reviewer` responsibility;
4. decide whether to request amendments, merge, or escalate.

## Structure

```text
team.yaml                    # identity-free roles, responsibilities, work bindings, and naming policy

docs/team.md                 # shared team operating instructions

roles/coordinator.md         # coordinator role playbook
roles/developer.md           # developer role playbook
roles/reviewer.md            # reviewer role playbook

home/coordinator/AGENTS.md   # coordinator home template
home/developer/AGENTS.md     # developer home template
home/reviewer/AGENTS.md      # reviewer home template
```

## Included team

| Responsibility | Identity scope | Role name | Work binding |
|---|---:|---:|---|
| Coordinator | local | `coordinator` | repo root |
| Developer | local | `developer` | git worktree |
| Reviewer | local | `reviewer` | git worktree |

Default naming policy:

- Local team aliases use `<identity-prefix>-<classic-name>`, for example `juan-alice`, `juan-bob`, `juan-charlie`.
- Global team aliases, for agents added later with `aw agents add --global`, use `<identity-prefix>-<classic-name>`.
- Global namespace addresses, for agents added later with `aw agents add --global`, use `<identity-prefix>-<responsibility>`.

For example, if Juan bootstraps with `--identity-prefix juan`, the default coordinator/developer/reviewer aliases are `juan-alice`, `juan-bob`, and `juan-charlie`. If Juan later adds a public global `support` responsibility, its namespace address can be `juan-support`. If Maria provisions the same committed layout later with `--identity-prefix maria`, she receives `maria-alice`, `maria-bob`, and `maria-charlie` with distinct DIDs, certificates, aliases, and any future global addresses without changing committed `team.yaml`.

## Second human on the same repo

Human A commits the generated layout:

```bash
git add agents .gitignore
git commit -m "Add aweb agents layout"
```

Human B clones the same repo and joins the same team with an invite:

```bash
git clone <repo-url>
cd <repo>
aw agents provision --invite-token "$AWEB_INVITE_TOKEN" --identity-prefix maria
```

Human B's private keys, DIDs, certificates, and local `.aw/` state are generated locally under `agents/home/*/.aw/` and are ignored by git. The committed `agents/team.yaml`, roles, docs, and home templates stay identity-free.

## BYOT example

Bring Your Own Team (BYOT, including your own namespace/domain controller):

```bash
aw agents bootstrap https://github.com/awebai/aweb-team-coord-worktrees.git \
  --aweb-url http://localhost:8000 \
  --registry http://localhost:8010 \
  --namespace example.com \
  --team coord-worktrees \
  --identity-prefix <your-name>
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
