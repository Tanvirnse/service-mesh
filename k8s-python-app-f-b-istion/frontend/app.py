from flask import Flask, render_template, request
import requests
import os
import time

# OTel Setup (similar to backend)
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

app = Flask(__name__)

# --- OpenTelemetry Configuration ---
APP_VERSION = os.environ.get("APP_VERSION", "v0.0-local")
POD_NAME = os.environ.get("POD_NAME", "local-dev-pod")
SERVICE_NAME = f"frontend-{APP_VERSION}"

# Setup tracing
otlp_exporter = OTLPSpanExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "otel-collector.istio-system:4317"),
    insecure=True
)
resource = Resource(attributes={"service.name": SERVICE_NAME})
provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(provider)

# Instrument Flask and Requests
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
# --- End OpenTelemetry Configuration ---

# Backend service URL. In K8s, this will be the service name.
BACKEND_SERVICE_URL = os.environ.get("BACKEND_SERVICE_URL", "http://localhost:8000")

def get_backend_data():
    try:
        # Check for Istio's trace headers and propagate them
        trace_headers = ['x-request-id', 'x-b3-traceid', 'x-b3-spanid', 'x-b3-parentspanid', 'x-b3-sampled', 'x-b3-flags']
        headers = {key: request.headers.get(key) for key in trace_headers if request.headers.get(key)}
        
        # Use v2-header to demonstrate Istio routing
        headers['x-app-version'] = 'v2' # Change to 'v1' to test routing

        response = requests.get(f"{BACKEND_SERVICE_URL}/api/data", headers=headers, timeout=5)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)

@app.route('/')
def index():
    backend_data, error = get_backend_data()
    return render_template('index.html', title='Home Page', pod_name=POD_NAME, app_version=APP_VERSION, backend_data=backend_data, error=error)

@app.route('/page2')
def page2():
    backend_data, error = get_backend_data()
    return render_template('page2.html', title='Page 2', pod_name=POD_NAME, app_version=APP_VERSION, backend_data=backend_data, error=error)

@app.route('/page3')
def page3():
    backend_data, error = get_backend_data()
    return render_template('page3.html', title='Page 3', pod_name=POD_NAME, app_version=APP_VERSION, backend_data=backend_data, error=error)

@app.route('/page4')
def page4():
    backend_data, error = get_backend_data()
    return render_template('page4.html', title='Page 4', pod_name=POD_NAME, app_version=APP_VERSION, backend_data=backend_data, error=error)

@app.route('/page5')
def page5():
    backend_data, error = get_backend_data()
    return render_template('page5.html', title='Page 5', pod_name=POD_NAME, app_version=APP_VERSION, backend_data=backend_data, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)