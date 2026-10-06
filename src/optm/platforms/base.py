from __future__ import annotations

from abc import ABC, abstractmethod


class Platform(ABC):
    name: str

    @abstractmethod
    def publish(self, text: str) -> str:
        """Publish text and return the platform's post id."""
