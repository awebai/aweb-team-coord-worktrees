# Creating a team from this blueprint

This repository is a **team blueprint**. It is not the user's team and it is
not the place where identities should be created.

If a human points you at this repo and asks you to create a team in a repo
they own:

1. Read `resource-pack.yaml` to discover the available souls, roles,
   playbooks, skills, docs, and adapters.
2. Load and follow `skills/create-team/SKILL.md`.
3. Treat `resources/souls/*` as durable agent bodies that are copied into the
   target repo and committed there — they are living state and grow with the
   team.
4. Treat `skills/spawn-instance` and `skills/self-maintenance` as procedures
   the finished team uses after installation; copy them into the target's
   `.agents/skills/`.
5. Use explicit aweb primitives and explicit filesystem/git steps. Do not run
   a monolithic bootstrap command, do not create hidden git worktrees, and do
   not copy `.aw` state.

The product motion is:

> Human chooses this blueprint; their agent copies the identity-free souls,
> roles, docs, and skills into the target repo and commits them, connects the
> first instance with explicit aweb primitives, publishes the shared
> instructions/roles, and hands the team to the human. The team then spawns
> further instances itself, when work needs them.

The agent applying this blueprint has no role in the finished team.
