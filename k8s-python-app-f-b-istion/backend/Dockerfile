FROM python:3.9-slim

WORKDIR /app

# Set environment variables for OpenTelemetry
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector.istio-system:4317"
ENV OTEL_RESOURCE_ATTRIBUTES="service.name=backend"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]