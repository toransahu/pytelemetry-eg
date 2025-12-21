from dataclasses import dataclass
from opentelemetry import trace


@dataclass(frozen=True)
class TelemetryContext:
    name: str
    env_prefix: str
    tracer_name: str

    def tracer(self):
        return trace.get_tracer(self.tracer_name)
