import os

import httpx

from .base import Platform


class FacebookPlatform(Platform):
    name = "facebook"

    def __init__(self, page_id: str):
        self.page_id = page_id
        self.token = os.environ["FACEBOOK_PAGE_TOKEN"]

    def publish(self, text: str) -> str:
        r = httpx.post(
            f"https://graph.facebook.com/v19.0/{self.page_id}/feed",
            data={"message": text, "access_token": self.token},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()["id"]
