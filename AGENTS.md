# Applying this team operating pattern

This repository is a source pattern. It is not the user's team and it is not the
place where identities should be created.

If a human points you at this repo and asks you to set up a team in a repo or
directory they own:

1. Read `resource-pack.yaml` to discover the available souls, roles, playbooks,
   skills, and adapters.
2. Load and follow `skills/apply-operating-pattern/SKILL.md`.
3. Treat `resources/souls/*` as durable agent bodies that can be copied into the
   target project.
4. Treat `skills/*` as procedures that target agents may use after the pattern is
   installed.
5. Use explicit aweb primitives and explicit filesystem/git steps. Do not run a
   monolithic bootstrap command, do not create hidden git worktrees, and do not
   copy `.aw` state.

The normal product motion is:

> Human chooses this operating pattern; their agent reads this repo, copies the
> identity-free souls/roles/skills into the target repo, connects concrete
> instances with aweb primitives, and publishes the shared instructions/roles.
