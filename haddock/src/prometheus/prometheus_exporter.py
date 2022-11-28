import os
from threading import Thread

from prometheus_client import Gauge, start_http_server, REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR, GC_COLLECTOR, \
    Info

from models.metrics import Metrics
from utils.utils import celcius_to_fahrenheit


class PrometheusExporter:
    def __init__(self) -> None:
        self.m_hostname_info = Info('hw611_hostname', 'Hostname of the HW611 sensor', ['hostname'])
        self.m_altitude_gauge = Gauge('hw611_altitude', 'Altitude measured by the HW611 sensor', ['hostname'])
        self.m_pressure_gauge = Gauge('hw611_pressure', 'Pressure measured by the HW611 sensor', ['hostname'])
        self.m_temperature_gauge = Gauge('hw611_temperature', 'Temperature measured by the HW611 sensor',
                                         ['hostname', 'scale'])

        REGISTRY.unregister(PROCESS_COLLECTOR)
        REGISTRY.unregister(PLATFORM_COLLECTOR)
        REGISTRY.unregister(GC_COLLECTOR)

    def update(self, metrics: Metrics) -> None:
        self.m_hostname_info.labels(hostname=metrics.hostname)
        self.m_altitude_gauge.labels(hostname=metrics.hostname).set(metrics.altitude)
        self.m_pressure_gauge.labels(hostname=metrics.hostname).set(metrics.pressure)
        self.m_temperature_gauge.labels(hostname=metrics.hostname, scale='celcius').set(metrics.temperature)
        self.m_temperature_gauge.labels(hostname=metrics.hostname, scale='fahrenheit') \
            .set(celcius_to_fahrenheit(metrics.temperature))

    @staticmethod
    def start() -> None:
        Thread(start_http_server(int(os.getenv('PROMETHEUS_EXPORTER_PORT')))).start()
