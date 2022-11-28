from pydantic import BaseModel


class Metrics(BaseModel):
    hostname: str
    altitude: float
    pressure: float
    temperature: float
