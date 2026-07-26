"""
Audit logging utilities for authentication and security events.
"""

import logging

logger = logging.getLogger("audit")


AuditContextValue = str | int | float | bool


def _compact_extra(extra: dict[str, AuditContextValue | None]) -> dict[str, AuditContextValue]:
    return {key: value for key, value in extra.items() if value is not None}


def log_auth_success(actor_id: str, method: str, path: str, **context: AuditContextValue) -> None:
    """Log successful authentication."""
    logger.info(
        "Authentication successful",
        extra=_compact_extra(
            {"event": "auth_success", "actor_id": actor_id, "method": method, "path": path, **context}
        ),
    )


def log_auth_failure(error: str, method: str, path: str, **context: AuditContextValue) -> None:
    """Log failed authentication."""
    logger.warning(
        "Authentication failed",
        extra=_compact_extra({"event": "auth_failure", "auth_error": error, "method": method, "path": path, **context}),
    )


def log_error(message: str, **kwargs: AuditContextValue) -> None:
    """Log an error with optional extra data."""
    logger.error(message, extra=kwargs)
