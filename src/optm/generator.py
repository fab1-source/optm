from __future__ import annotations

from .config import Company

# Conservative per-platform character limits.
LIMITS = {"x": 280, "linkedin": 3000, "facebook": 2000}

PLATFORM_STYLE = {
    "x": "A single punchy post. Max 280 characters including hashtags. At most 2 hashtags.",
    "linkedin": "A professional post of 600-1200 characters, short paragraphs, 2-4 hashtags at the end.",
    "facebook": "A conversational post of 200-600 characters, optional question to spark comments.",
}


def build_prompt(company: Company, platform: str, topic: str, recent: list[str]) -> str:
    recent_block = "\n".join(f"- {t[:200]}" for t in recent) or "(none yet)"
    avoid = ", ".join(company.avoid) or "nothing in particular"
    return f"""Write one social media post for {company.name}.

About the company: {company.description}
Audience: {company.audience}
Tone: {company.tone}
Topic for this post: {topic}
Preferred hashtags: {' '.join(company.hashtags) or '(none)'}
Never touch on: {avoid}

Platform: {platform}. {PLATFORM_STYLE.get(platform, '')}

Recent posts (do NOT repeat their ideas or phrasing):
{recent_block}

Rules: do not invent statistics, prices, discounts, customer quotes or events.
Output ONLY the post text, with no preamble, quotes or explanation."""


class Generator:
    def __init__(self, model: str, client=None):
        self.model = model
        if client is None:
            import anthropic

            client = anthropic.Anthropic()
        self.client = client

    def generate(self, company: Company, platform: str, topic: str, recent: list[str]) -> str:
        limit = LIMITS.get(platform, 1000)
        prompt = build_prompt(company, platform, topic, recent)
        for _ in range(3):
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            text = "".join(b.text for b in resp.content if b.type == "text").strip()
            if text and len(text) <= limit:
                return text
            prompt += f"\n\nYour last draft was {len(text)} characters; the limit is {limit}. Make it shorter."
        raise ValueError(f"could not produce a post within {limit} characters")
