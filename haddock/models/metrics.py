from pydantic import BaseModel


class Metrics(BaseModel):
    altitude: float
    pressure: float
    temperature: float
