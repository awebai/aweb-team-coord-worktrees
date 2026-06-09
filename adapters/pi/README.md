# Pi adapter

Pi runs from any instance home: create/connect the instance first, then
launch `pi` from that directory after linking the soul's `AGENTS.md`. Pi
reads skills from `.agents/skills`.

For message wake-up, install the aweb extension once per machine:

```bash
pi install npm:@awebai/pi@latest
```

Reviewers are good Pi candidates because reviewing on a different runtime
than the code's author helps preserve fresh eyes — this blueprint's reviewer
soul declares `runtime: pi`.
