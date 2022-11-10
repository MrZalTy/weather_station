import os

import uvicorn
from fastapi import FastAPI

from prometheus.prometheus_exporter import PrometheusExporter
from routes.metrics import metrics_router


def main():
    app = FastAPI(title="Haddock API",
                  description="API Documentation for Haddock",
                  version="1.0.0", openapi_tags=[{"name": "metrics", "description": "Metrics module"}])
    app.state.prometheus_exporter = PrometheusExporter()

    app.include_router(metrics_router)

    app.state.prometheus_exporter.start()
    uvicorn.run(app, host=os.getenv('API_HOST'), port=int(os.getenv('API_PORT')))


if __name__ == "__main__":
    main()
