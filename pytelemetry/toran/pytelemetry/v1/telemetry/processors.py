from opentelemetry.sdk.trace import SpanProcessor


class ComponentFilteringSpanProcessor(SpanProcessor):
    """
    Routes spans to a delegate processor based on span attribute.
    """

    def __init__(self, delegate: SpanProcessor, component: str):
        self._delegate = delegate
        self._component = component

    def on_start(self, span, parent_context=None):
        pass

    def on_end(self, span):
        if span.attributes.get("component") == self._component:
            self._delegate.on_end(span)

    def shutdown(self):
        self._delegate.shutdown()

    def force_flush(self, timeout_millis: int = 30000):
        self._delegate.force_flush(timeout_millis)
