from types import SimpleNamespace

from optm.config import Config
from optm.db import Store
from optm.generator import Generator
from optm.pipeline import run_once


class FakeClient:
    def __init__(self, replies):
        self.replies = list(replies)
        self.messages = self

    def create(self, **kw):
        t = self.replies.pop(0)
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=t)])


def make_cfg(dry=True):
    return Config.model_validate({
        "company": {"name": "Acme", "description": "d", "topics": ["a", "b"]},
        "dry_run": dry,
        "platforms": {"x": {"cron": "0 9 * * *"}},
    })


def test_retries_when_too_long():
    gen = Generator("m", FakeClient(["x" * 300, "short"]))
    assert gen.generate(make_cfg().company, "x", "a", []) == "short"


def test_dry_run_records_and_rotates_topics():
    store = Store(":memory:")
    gen = Generator("m", FakeClient(["one", "two"]))
    cfg = make_cfg()
    run_once(cfg, "x", store, gen)
    run_once(cfg, "x", store, gen)
    rows = store.conn.execute("SELECT topic, status FROM posts ORDER BY id").fetchall()
    assert rows == [("a", "dry_run"), ("b", "dry_run")]


def test_failure_is_recorded_not_raised():
    store = Store(":memory:")
    gen = Generator("m", FakeClient([]))  # pop from empty -> error
    assert run_once(make_cfg(), "x", store, gen) is None
    assert store.conn.execute("SELECT status FROM posts").fetchone()[0] == "failed"
