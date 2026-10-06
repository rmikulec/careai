"""OpenTelemetry tracing setup for the CareAI API.

Wires a single self-hosted OTLP pipeline: a ``TracerProvider`` exporting spans
over gRPC to an OTLP endpoint (a local Jaeger/collector in the dev stack), with
automatic instrumentation for FastAPI requests and the SQLAlchemy engine. The
reporting agent adds its own per-stage spans via ``opentelemetry.trace`` (a no-op
until this configures a real provider), so agent code carries no hard dependency
on telemetry being enabled.

Tracing is off unless ``OTEL_ENABLED`` is set (see :class:`CareAI.config.Settings`),
so local uvicorn runs and the test suite don't attempt to reach an exporter. No
span records message content or PHI — only structural attributes (phase names,
counts, tool names).
"""

import logging

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from CareAI.config import Settings
from CareAI.database.session import engine

logger = logging.getLogger(__name__)

# Guards the process-global setup (provider + SQLAlchemy instrumentation) so
# building more than one app in a process — as the tests do — configures it once.
_configured = False


def configure_telemetry(app: FastAPI, settings: Settings) -> None:
    """Configure OpenTelemetry tracing for the application.

    Installs a global ``TracerProvider`` exporting to the configured OTLP
    endpoint and instruments the FastAPI app and SQLAlchemy engine. A no-op when
    ``settings.otel_enabled`` is false, so tracing is opt-in per environment.

    Args:
        app (FastAPI): The application whose requests should be traced.
        settings (Settings): Runtime settings providing the OTEL toggle,
            endpoint, and service name.
    """
    global _configured
    if not settings.otel_enabled:
        logger.debug("OpenTelemetry disabled; skipping tracing setup")
        return

    if not _configured:
        resource = Resource.create(
            {
                SERVICE_NAME: settings.otel_service_name,
                SERVICE_VERSION: app.version,
            }
        )
        provider = TracerProvider(resource=resource)
        # gRPC over a plaintext dev endpoint (``http://``) needs insecure=True;
        # a TLS endpoint (``https://``) uses the default secure channel.
        insecure = settings.otel_exporter_otlp_endpoint.startswith("http://")
        exporter = OTLPSpanExporter(
            endpoint=settings.otel_exporter_otlp_endpoint, insecure=insecure
        )
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)
        # The async engine wraps a sync Engine that the instrumentation hooks.
        SQLAlchemyInstrumentor().instrument(
            engine=engine.sync_engine, tracer_provider=provider
        )
        _configured = True
        logger.info(
            "OpenTelemetry tracing enabled (service=%s, endpoint=%s)",
            settings.otel_service_name,
            settings.otel_exporter_otlp_endpoint,
        )

    # Per-app: safe to call once per FastAPI instance.
    FastAPIInstrumentor.instrument_app(app)
