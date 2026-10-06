from __future__ import annotations

import argparse
import logging

from .config import load_config
from .db import Store
from .generator import Generator
from .pipeline import run_once
from .scheduler import build_scheduler


def main() -> None:
    p = argparse.ArgumentParser(prog="optm")
    p.add_argument("-c", "--config", default="config.yaml")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("run", help="start the fully automated scheduler")
    now = sub.add_parser("post-now", help="generate and post once, immediately")
    now.add_argument("platform")
    sub.add_parser("history", help="show recent posts")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    cfg = load_config(args.config)
    store = Store(cfg.database)

    if args.cmd == "history":
        for created, platform, status, text in store.history():
            print(f"{created[:19]} [{platform}/{status}] {text[:100]!r}")
        return

    gen = Generator(cfg.model)
    if args.cmd == "post-now":
        run_once(cfg, args.platform, store, gen)
    else:
        sched = build_scheduler(cfg, store, gen)
        mode = "DRY-RUN" if cfg.dry_run else "LIVE"
        logging.info("scheduler started (%s) for: %s", mode, ", ".join(j.id for j in sched.get_jobs()))
        try:
            sched.start()
        except (KeyboardInterrupt, SystemExit):
            pass


if __name__ == "__main__":
    main()
