import json
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
            log_data = {
                    "name": span.name,
                    "duration_ms": round(duration_ms, 2),
                    "trace_id": hex(span.context.trace_id),
                    "span_id": hex(span.context.span_id),
                    "parent_span_id": hex(span.parent.span_id) if span.parent else None,
                    "component": span.attributes.get("component", "unknown"),
                    "function": span.attributes.get("function"),
                    "start_time": span.start_time,
                    "end_time": span.end_time,
                }
            self._logger.info(json.dumps(log_data))
        return SpanExportResult.SUCCESS

    def shutdown(self):
        pass
