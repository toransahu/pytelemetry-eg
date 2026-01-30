import functools
from typing import Optional

from toran.pytelemetry.v1.instrumentation.context import TelemetryContext
from toran.pytelemetry.v1.instrumentation.controls import instrumentation_enabled


def traceit(
    ctx: TelemetryContext,
    *,
    name: Optional[str] = None,
    record_args: bool = True,
    record_kwargs: bool = True,
    filter_kwargs: list[str] | None = None,
):
    """
    Context-aware tracing decorator.

    :params ctx: TelemetryContext
    :params name: Given name of the span (defaults to function name)
    :params record_args: Should record the function arguments?
    :params record_kwargs: Should record the function keyworded arguments?
    :params filter_kwargs: Only fields in the function keyworded arguments to record
    :returns: Decorator
    """

    def decorator(fn):
        span_name = name or fn.__qualname__

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if not instrumentation_enabled(ctx):
                return fn(*args, **kwargs)

            tracer = ctx.tracer()
            with tracer.start_as_current_span(span_name) as span:
                span.set_attribute("scope", span.instrumentation_scope.name)
                span.set_attribute("module", fn.__module__)
                span.set_attribute("function", fn.__qualname__)
                if record_args and args:
                    span.set_attribute("fn_args", args)
                _kwargs = kwargs
                if kwargs and filter_kwargs:
                    _kwargs = {k: v for k, v in kwargs.items() if k in filter_kwargs}
                if record_kwargs and _kwargs:
                    for k, v in _kwargs.items():
                        span.set_attribute(f"fn_{k}", v)
                return fn(*args, **kwargs)

        return wrapper

    return decorator
