from __future__ import annotations

import logging

from .config import Config
from .db import Store
from .generator import Generator
from .platforms import REGISTRY

log = logging.getLogger("optm")


def run_once(cfg: Config, name: str, store: Store, gen: Generator) -> str | None:
    """Generate and publish one post for a platform. Never raises, so the scheduler keeps going."""
    topics = cfg.company.topics
    topic = topics[store.count(name) % len(topics)]
    text = ""
    try:
        text = gen.generate(cfg.company, name, topic, store.recent_texts(name))
        if cfg.dry_run:
            log.info("[dry-run] %s: %s", name, text)
            store.add(name, topic, text, "dry_run")
            return text
        pcfg = cfg.platforms[name]
        ext_id = REGISTRY[name](pcfg.page_id).publish(text)
        store.add(name, topic, text, "published", external_id=str(ext_id))
        log.info("published %s post %s", name, ext_id)
        return text
    except Exception as e:  # noqa: BLE001 - one failed run must not stop automation
        log.exception("run failed for %s", name)
        store.add(name, topic, text, "failed", error=str(e))
        return None
