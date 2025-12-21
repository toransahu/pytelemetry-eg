from toran.pytelemetry.v1.instrumentation.context import TelemetryContext

LIB_CTX = TelemetryContext(
    name="sample_lib1",
    env_prefix="SAMPLE_LIB1",
    tracer_name="sample_lib1",
)
