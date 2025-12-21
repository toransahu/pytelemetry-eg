import functools
from typing import Optional

from toran.pytelemetry.v1.instrumentation.context import TelemetryContext
from toran.pytelemetry.v1.instrumentation.controls import instrumentation_enabled


def traceit(
    ctx: TelemetryContext,
    *,
    name: Optional[str] = None,
):
    """
    Context-aware tracing decorator.
    """

    def decorator(fn):
        span_name = name or fn.__qualname__

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if not instrumentation_enabled(ctx):
                return fn(*args, **kwargs)

            tracer = ctx.tracer()
            with tracer.start_as_current_span(span_name) as span:
                span.set_attribute("component", ctx.name)
                span.set_attribute("function", fn.__qualname__)
                return fn(*args, **kwargs)

        return wrapper

    return decorator
