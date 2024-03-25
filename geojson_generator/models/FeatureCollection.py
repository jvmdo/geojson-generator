from pydantic import BaseModel
from typing import List, Union


class Coordinates(BaseModel):
    coordinates: List[List[float | str]]
    # type: str


class Geometry(BaseModel):
    coordinates: Coordinates
    type: str


class Properties(BaseModel):
    name: str
    startDateTime: str
    endDateTime: str


class Feature(BaseModel):
    type: str
    properties: Properties
    geometry: Geometry
    # id: int


class FeatureCollection(BaseModel):
    type: str
    features: List[Feature]
