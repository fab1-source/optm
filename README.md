# optm — automated social media marketing

One-time setup, then fully automatic: on each platform's cron schedule, `optm` asks Claude to write
an on-brand post (rotating topics, avoiding repeats of recent posts), publishes it, and logs it in SQLite.

## Setup
```
python -m venv .venv && . .venv/bin/activate && pip install -e .
cp config.example.yaml config.yaml   # company profile, platforms, schedules
cp .env.example .env                 # API keys (export them in your environment)
```
## Use
```
optm post-now x     # try one post (dry_run: true only logs it)
optm run            # start the scheduler; runs forever
optm history
```
Keep `dry_run: true` until you've reviewed a few generated posts, then set it to `false`.
Run `optm run` under systemd/Docker/a process manager so it restarts on failure.

## Platforms
X, LinkedIn (organization pages) and Facebook Pages. Add one by implementing `Platform.publish`
in `src/optm/platforms/` and registering it. Note: X OAuth2 user tokens expire (~2h) unless refreshed;
token refresh is not yet implemented.
