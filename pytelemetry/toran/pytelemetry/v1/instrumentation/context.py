from dataclasses import dataclass
from opentelemetry import trace


@dataclass(frozen=True)
class TelemetryContext:
    name: str

    def tracer(self):
        return trace.get_tracer(self.name)

    @property
    def env_var_name(self) -> str:
        return f"{self.name.upper().replace('-', '_')}_TELEMETRY_ENABLED"
