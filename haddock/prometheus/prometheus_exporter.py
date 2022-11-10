import os
from threading import Thread

from prometheus_client import Gauge, start_http_server

from models.metrics import Metrics
from utils.utils import celcius_to_fahrenheit


class PrometheusExporter:
    def __init__(self) -> None:
        self.gauge_altitude = Gauge('hw611_altitude', 'Altitude measured by the HW611 sensor')
        self.gauge_pressure = Gauge('hw611_pressure', 'Pressure measured by the HW611 sensor')
        self.gauge_temperature = Gauge('hw611_temperature', 'Temperature measured by the HW611 sensor', ['scale'])

        self.gauge_temperature.labels('celcius')
        self.gauge_temperature.labels('fahrenheit')

    def update(self, metrics: Metrics) -> None:
        self.gauge_altitude.set(metrics.altitude)
        self.gauge_pressure.set(metrics.pressure)
        self.gauge_temperature.labels('celcius').set(metrics.temperature)
        self.gauge_temperature.labels('fahrenheit').set(celcius_to_fahrenheit(metrics.temperature))

    @staticmethod
    def start() -> None:
        Thread(start_http_server(int(os.getenv('PROMETHEUS_EXPORTER_PORT')))).start()
