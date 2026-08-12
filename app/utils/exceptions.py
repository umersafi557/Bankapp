from typing import Any


class BusinessRuleError(Exception):
    def __init__(self, message: str, details: Any = None) -> None:
        super().__init__(message)
        self.details = details


class NotFoundError(Exception):
    pass


class UnauthorizedError(Exception):
    pass
