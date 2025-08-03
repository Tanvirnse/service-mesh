FROM python:3.9-slim

WORKDIR /app

# Set environment variables for OpenTelemetry
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector.istio-system:4317"
ENV OTEL_RESOURCE_ATTRIBUTES="service.name=frontend"

# Set backend URL for K8s service discovery
ENV BACKEND_SERVICE_URL="http://backend-service.istio-apps:8000"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--port", "5000"]