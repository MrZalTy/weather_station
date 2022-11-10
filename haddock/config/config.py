import os

api_host: str = os.getenv('API_HOST')
api_port: int = int(os.getenv('API_PORT'))

prometheus_port: int = int(os.getenv('PROMETHEUS_PORT'))
