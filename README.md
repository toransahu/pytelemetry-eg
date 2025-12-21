# PyTelemetry Monorepo (uv + OpenTelemetry)

This repository demonstrates:
1. A true **monorepos** design & structure
1. A **DRY, first-party telemetry architecture** using **OpenTelemetry**, designed for multiple Python libraries and services.

It shows how:
- A **shared telemetry core** (`pytelemetry`) can be reused
- Each **library / service controls its own instrumentation**
- **Exporters are decided by the consuming service**
- Everything is controlled via **environment variables**
- No reinvention of OpenTelemetry primitives

---

## Repository Layout

```
.
├── pyproject.toml              # Workspace root (uv)
├── pytelemetry                 # Shared telemetry core
│   ├── pyproject.toml
│   └── toran
│       └── pytelemetry
│           ├── __init__.py
│           └── v1
│               ├── instrumentation
│               └── telemetry
│
├── sample_lib1                 # First-party library
│   ├── pyproject.toml
│   └── toran
│       └── sample_lib1
│           └── v1
│
├── sample_service1             # First-party service
│   ├── pyproject.toml
│   └── sample_service1
│       ├── app.py
│       └── telemetry.py
│
├── README.md                   # This file
└── uv.lock
```

---

## Requirements

- Python **3.10+**
- [`uv`](https://github.com/astral-sh/uv)

---

## Initial Setup

From repo root:

```bash
uv sync
```

---

## Validate Installation

```bash
uv run python - <<EOF
import toran.pytelemetry
import toran.sample_lib1
import sample_service1
print("All imports OK")
EOF
```

---

## Running the Service

```bash
uv run python -m sample_service1.app
```

## Running the Lib

```bash
uv run python -m toran.sample_lib1.v1.core
```

---

## Environment Variables

| Project | Variable |
|-------|---------|
| sample_lib1 | `SAMPLE_LIB1_TELEMETRY_ENABLED` |
| sample_service1 | `SAMPLE_SERVICE1_TELEMETRY_ENABLED` |

Accepted values:

```
true | 1 | yes
false | 0 | no
```

---

## Disable Telemetry Example

```bash
export SAMPLE_LIB1_TELEMETRY_ENABLED=false
uv run python -m sample_service1.app
```

---
# How Instrumentation Works

## Decorator

```python
@traceit(LIB_CTX)
def compute():
    ...
```

- No tracer setup in the library
- No exporter decisions
- Fully controlled by environment

## Runtime Behavior

| Condition          | Result                          |
| ------------------ | ------------------------------- |
| Telemetry disabled | Function executes normally      |
| Telemetry enabled  | Span created + nested correctly |
| Exporter missing   | No-op (safe)                    |

---

# Exporter Selection

## Default behavior

`pytelemetry` ships with minimal console exporter

Intended for:

- local development
- learning
- debugging

## Service-level override (recommended)

Services may replace exporters in their own telemetry setup:

```python
# sample_service1/telemetry.py
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace

def setup_service_telemetry():
    provider = TracerProvider()
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter())
    )
    trace.set_tracer_provider(provider)
```

This:

- Affects all spans
- Keeps instrumentation code unchanged
- Matches real production usage

---

## Design Principles

- ✅ No OpenTelemetry API reimplementation
- ✅ No hard-coded exporters in libraries
- ✅ Per-project enable/disable
- ✅ Monorepo-friendly
- ✅ PyPI-ready namespace (toran.*)
- ✅ Versioned (v1, future v2, etc.)

---

## Future Extensions

- Metrics (`MeterProvider`)
- Log signal integration
- Span filtering by component
- Context propagation helpers
- `pytest` span assertions

---

## Summary

This setup mirrors real-world OSS telemetry usage:
- Libraries emit signals
- Services decide destinations
- Ops control behavior via env vars
- No OpenTelemetry API duplication
- Zero vendor lock-in
- Clean separation of concerns
- Production-safe defaults
- Monorepo-friendly
