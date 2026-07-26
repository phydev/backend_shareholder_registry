"""
JSON logging formatter for SPLUNK audit log ingestion.
"""

import json
import logging
from datetime import UTC, datetime


class AuditJSONFormatter(logging.Formatter):
    """JSON formatter that outputs SPLUNK-compatible audit logs."""

    EXTRA_FIELDS = [
        "event",
        "actor_id",
        "actor_oid",
        "status_code",
        "method",
        "path",
        "auth_error",
        "outcome",
        "reason_code",
        "correlation_id",
        "client_ip",
        "forwarded_for",
        "user_agent",
        "client_app_id",
    ]

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "application": "brreg",
        }

        # Add specific extra fields from the "extra" parameter in logging calls
        log_entry.update({field: getattr(record, field) for field in self.EXTRA_FIELDS if hasattr(record, field)})

        return json.dumps(log_entry, ensure_ascii=False)
