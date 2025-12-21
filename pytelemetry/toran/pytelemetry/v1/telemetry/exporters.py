import logging
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult


class SimpleLogSpanExporter(SpanExporter):
    """
    Beginner-friendly exporter.
    """

    def __init__(self, logger_name: str):
        self._logger = logging.getLogger(logger_name)

    def export(self, spans):
        for span in spans:
            # Calculate duration in milliseconds
            duration_ns = span.end_time - span.start_time
            duration_ms = duration_ns / 1_000_000  # Convert nanoseconds to milliseconds
            self._logger.info(
                "SPAN name=%s duration=%.2fms trace_id=%s span_id=%s parent=%s component=%s",
                span.name,
                duration_ms,
                hex(span.context.trace_id),
                hex(span.context.span_id),
                hex(span.parent.span_id) if span.parent else None,
                span.attributes.get("component", "unknown"),
            )
        return SpanExportResult.SUCCESS

    def shutdown(self):
        pass
