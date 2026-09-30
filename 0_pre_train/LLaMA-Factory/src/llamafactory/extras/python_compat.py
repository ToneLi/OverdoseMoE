"""Compatibility helpers for running the bundled source on Python 3.10."""

try:
    from enum import StrEnum as StrEnum
except ImportError:  # StrEnum was added in Python 3.11.
    from enum import Enum

    class StrEnum(str, Enum):
        """Subset of enum.StrEnum required by LLaMA-Factory."""

        def __str__(self) -> str:
            return str(self.value)

