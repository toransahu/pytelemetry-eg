from opentelemetry import trace
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace import TracerProvider
from toran.pytelemetry.v1.instrumentation.context import TelemetryContext
from toran.pytelemetry.v1.telemetry.exporters import SimpleLogSpanExporter


SERVICE_CTX = TelemetryContext(
    name="sample_service1",
)


def setup_telemetry():
    provider = TracerProvider()

    # exporter and processor for all
    span_processor = SimpleSpanProcessor(
        SimpleLogSpanExporter()
    )
    provider.add_span_processor(span_processor)

    trace.set_tracer_provider(provider)
