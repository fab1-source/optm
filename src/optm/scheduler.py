from __future__ import annotations

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from .config import Config
from .db import Store
from .generator import Generator
from .pipeline import run_once


def build_scheduler(cfg: Config, store: Store, gen: Generator) -> BlockingScheduler:
    sched = BlockingScheduler(timezone=cfg.timezone)
    for name, pcfg in cfg.platforms.items():
        if not pcfg.enabled:
            continue
        sched.add_job(
            run_once,
            CronTrigger.from_crontab(pcfg.cron, timezone=cfg.timezone),
            args=[cfg, name, store, gen],
            id=name,
            misfire_grace_time=3600,
            coalesce=True,
        )
    return sched
