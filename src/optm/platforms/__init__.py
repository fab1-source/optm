from .base import Platform
from .facebook import FacebookPlatform
from .linkedin import LinkedInPlatform
from .x import XPlatform

REGISTRY: dict[str, type[Platform]] = {
    "x": XPlatform,
    "linkedin": LinkedInPlatform,
    "facebook": FacebookPlatform,
}

__all__ = ["Platform", "REGISTRY"]
