import os
from toran.pytelemetry.v1.instrumentation.context import TelemetryContext


def instrumentation_enabled(ctx: TelemetryContext) -> bool:
    return os.getenv(ctx.env_var_name, "true").lower() in ("1", "true", "yes")
