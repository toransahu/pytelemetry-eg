import json
import logging
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult


class SimpleLogSpanExporter(SpanExporter):
    """
    Beginner-friendly exporter.
    """

    def export(self, spans):
        for span in spans:
            # Get scope from instrumentation_scope (built-in)
            scope = span.instrumentation_scope.name if span.instrumentation_scope else "unknown"
            # Get module name
            module = span.attributes.get("module", "")
            # Get logger
            logger_name = module if module else scope
            self.logger = logging.getLogger(logger_name)
            # Calculate duration in milliseconds
            duration_ns = span.end_time - span.start_time
            duration_ms = duration_ns / 1_000_000  # Convert nanoseconds to milliseconds
            log_data = {
                    "name": span.name,
                    "scope": scope,  # e.g. "sample_lib1"
                    "module": module,  # e.g. "toran.sample_lib1.v1.core"
                    "function": span.attributes.get("function"), # e.g. "compute"
                    "duration_ms": round(duration_ms, 2),
                    "trace_id": hex(span.context.trace_id),
                    "span_id": hex(span.context.span_id),
                    "parent_span_id": hex(span.parent.span_id) if span.parent else None,
                    "start_time": span.start_time,
                    "end_time": span.end_time,
                }
            # TODO: Explore ReadableSpan.to_json() to get most of the info
            self.logger.info(json.dumps(log_data))
        return SpanExportResult.SUCCESS

    def shutdown(self):
        pass
