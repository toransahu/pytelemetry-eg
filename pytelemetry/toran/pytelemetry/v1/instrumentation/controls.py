import os
from toran.pytelemetry.v1.instrumentation.context import TelemetryContext


def instrumentation_enabled(ctx: TelemetryContext) -> bool:
    env_key = f"{ctx.env_prefix}_TELEMETRY_ENABLED"
    return os.getenv(env_key, "true").lower() in ("1", "true", "yes")
