from __future__ import annotations

from contextlib import contextmanager


def tracer(service_name: str = "self-healing-devops-agent"):
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
        trace.set_tracer_provider(provider)
        return trace.get_tracer(service_name)
    except ImportError:
        return None


@contextmanager
def span(name: str, **attributes):
    current = tracer()
    if current is None:
        yield None
        return
    with current.start_as_current_span(name) as active:
        for key, value in attributes.items():
            active.set_attribute(key, str(value))
        yield active
