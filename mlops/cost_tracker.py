from dataclasses import dataclass, field
from typing import List


@dataclass
class TokenUsage:
    model: str
    prompt_tokens: int
    completion_tokens: int

    @property
    def total(self) -> int:
        return self.prompt_tokens + self.completion_tokens


_log: List[TokenUsage] = []


def record(usage: TokenUsage) -> None:
    _log.append(usage)


def summary() -> dict:
    return {
        "calls": len(_log),
        "total_tokens": sum(u.total for u in _log),
    }
