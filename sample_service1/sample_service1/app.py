from toran.pytelemetry.v1.telemetry.setup import setup_telemetry
from toran.pytelemetry.v1.instrumentation.traceit import traceit
from toran.sample_lib1.v1.core import compute

from sample_service1.telemetry import SERVICE_CTX


@traceit(SERVICE_CTX)
def handler():
    return compute()


if __name__ == "__main__":
    setup_telemetry()
    handler()
