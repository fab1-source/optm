import os

import httpx

from .base import Platform


class LinkedInPlatform(Platform):
    name = "linkedin"

    def __init__(self, page_id: str):
        self.token = os.environ["LINKEDIN_ACCESS_TOKEN"]
        self.author = f"urn:li:organization:{page_id}"

    def publish(self, text: str) -> str:
        r = httpx.post(
            "https://api.linkedin.com/v2/ugcPosts",
            headers={
                "Authorization": f"Bearer {self.token}",
                "X-Restli-Protocol-Version": "2.0.0",
            },
            json={
                "author": self.author,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": text},
                        "shareMediaCategory": "NONE",
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
            },
            timeout=30,
        )
        r.raise_for_status()
        return r.json().get("id", r.headers.get("x-restli-id", ""))
