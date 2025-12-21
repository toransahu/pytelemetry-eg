from toran.pytelemetry.v1.instrumentation.context import TelemetryContext

SERVICE_CTX = TelemetryContext(
    name="sample_service1",
    env_prefix="SAMPLE_SERVICE1",
    tracer_name="sample_service1",
)
