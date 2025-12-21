from opentelemetry import trace
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace import TracerProvider
from toran.pytelemetry.v1.instrumentation.context import TelemetryContext
from toran.pytelemetry.v1.telemetry.exporters import SimpleLogSpanExporter
from toran.pytelemetry.v1.telemetry.processors import ComponentFilteringSpanProcessor


SERVICE_CTX = TelemetryContext(
    name="sample_service1",
    env_prefix="SAMPLE_SERVICE1",
    tracer_name="sample_service1",
)


def setup_telemetry():
    provider = TracerProvider()

    # exporter for library spans
    lib_exporter = SimpleSpanProcessor(
        SimpleLogSpanExporter("sample_lib1")
    )
    # exporter for service spans
    svc_exporter = SimpleSpanProcessor(
        SimpleLogSpanExporter("sample_service1")
    )
    provider.add_span_processor(
        ComponentFilteringSpanProcessor(lib_exporter, component="sample_lib1")
    )
    provider.add_span_processor(
        ComponentFilteringSpanProcessor(svc_exporter, component="sample_service1")
    )
    trace.set_tracer_provider(provider)
