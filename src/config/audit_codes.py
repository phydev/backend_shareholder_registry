"""Canonical codebook for audit outcomes and authentication reason codes."""

from enum import StrEnum


class AuditOutcome(StrEnum):
    SUCCESS = "success"
    DENIED = "denied"


class AuthReasonCode(StrEnum):
    AUTH_SUCCESS = "auth_success"
    MISSING_TOKEN = "missing_token"
    MALFORMED_AUTH_HEADER = "malformed_auth_header"
    INVALID_TOKEN = "invalid_token"
    MISSING_CLAIM = "missing_claim"
    INVALID_EXP = "invalid_exp"
    INVALID_AUDIENCE = "invalid_audience"
    EXPIRED_TOKEN = "expired_token"
    INVALID_CLIENT_APP_ID = "invalid_client_app_id"
    PERMISSION_DENIED = "permission_denied"
