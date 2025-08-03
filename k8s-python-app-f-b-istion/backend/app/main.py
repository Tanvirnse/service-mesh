from fastapi import FastAPI
from . import database, cache, dependencies
import os
import time

# Get app version from environment variable
APP_VERSION = os.environ.get("APP_VERSION", "v0.0-local")
POD_NAME = os.environ.get("POD_NAME", "local-dev-pod")
SERVICE_NAME = f"backend-{APP_VERSION}"

# Setup tracing before instrumenting
dependencies.setup_tracing(SERVICE_NAME)

app = FastAPI()

# Instrument FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
FastAPIInstrumentor.instrument_app(app)

# Instrument other libraries
from opentelemetry.instrumentation.requests import RequestsInstrumentor
RequestsInstrumentor().instrument()

from opentelemetry.instrumentation.redis import RedisInstrumentor
RedisInstrumentor().instrument()


@app.get("/api/data")
def get_data():
    start_time = time.time()
    
    db_conn = database.get_db_connection()
    db_data = database.get_db_data(db_conn)
    
    redis_conn = cache.get_redis_connection()
    redis_data = cache.get_redis_data(redis_conn)
    
    processing_time = (time.time() - start_time) * 1000

    return {
        "pod_name": POD_NAME,
        "app_version": APP_VERSION,
        "source": "backend",
        "database_info": db_data,
        "cache_info": redis_data,
        "processing_time_ms": round(processing_time, 2)
    }