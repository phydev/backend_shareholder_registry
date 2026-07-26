from django.http import HttpRequest
from drf_spectacular.generators import SchemaGenerator


def add_bearer_auth_scheme(
    result: dict[str, dict], generator: SchemaGenerator, request: HttpRequest, public: bool
) -> dict[str, dict]:
    """
    Postprocessing hook that injects a BearerAuth (JWT) security scheme into the
    generated OpenAPI schema and applies it globally to all operations.

    This is needed because AuroraAuthentication is a Django middleware (not a DRF
    authentication class), so drf-spectacular cannot auto-detect it.
    """
    result.setdefault("components", {})
    result["components"].setdefault("securitySchemes", {})
    result["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Paste your Bearer token (application/STS token from OpenShift pod) here.",
    }

    # Apply BearerAuth globally to every operation so the lock icon appears on each endpoint.
    for path_item in result.get("paths", {}).values():
        for operation in path_item.values():
            if isinstance(operation, dict):
                operation["security"] = [{"BearerAuth": []}]

    return result
