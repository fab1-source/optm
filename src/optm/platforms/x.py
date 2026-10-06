import os

import httpx

from .base import Platform


class XPlatform(Platform):
    name = "x"

    def __init__(self, page_id: str = ""):
        self.token = os.environ["X_ACCESS_TOKEN"]

    def publish(self, text: str) -> str:
        r = httpx.post(
            "https://api.twitter.com/2/tweets",
            headers={"Authorization": f"Bearer {self.token}"},
            json={"text": text},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()["data"]["id"]
