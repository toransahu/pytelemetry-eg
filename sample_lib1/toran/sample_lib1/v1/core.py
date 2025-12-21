from toran.pytelemetry.v1.telemetry.setup import setup_telemetry
from toran.pytelemetry.v1.instrumentation.traceit import traceit
from toran.sample_lib1.v1.telemetry import LIB_CTX


@traceit(LIB_CTX)
def compute() -> int:
    return 42


if __name__ == "__main__":
    setup_telemetry()
    compute()
