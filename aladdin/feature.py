from dataclasses import dataclass
from typing import Any

from aladdin.codable import Codable

class Constraint(Codable):
    name: str

    def to_dict(self) -> dict:
        return {"name": self.name}

    def __hash__(self) -> int:
        return hash(self.name)

@dataclass
class Above(Constraint):
    value: Any
    name = "above"

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class FeatureType(Codable):
    # FIXME: Should use a more Pythonic design, as this one did not behave as intended

    name: str

    @property
    def python_type(self) -> type:
        from uuid import UUID
        from numpy import double
        from datetime import datetime, date, time, timedelta
        return {
            "string": str,
            "int32": int,
            "int64": int,
            "float": float,
            "double": double,
            "bool": bool,
            "date": date,
            "datetime": datetime,
            "time": time,
            "timedelta": timedelta,
            "uuid": UUID,
            "array": list
        }[self.name]

    @property
    def pandas_type(self) -> type:
        from uuid import UUID
        import numpy as np
        return {
            "string": str,
            "int32": np.int32,
            "int64": np.int64,
            "float": np.float64,
            "double": np.double,
            "bool": np.bool8,
            "date": np.datetime64,
            "datetime": np.datetime64,
            "time": np.datetime64,
            "timedelta": np.timedelta64,
            "uuid": UUID,
            "array": list
        }[self.name]

    def __eq__(self, other: "FeatureType") -> bool:
        return self.name == other.name

    @property
    def string(self) -> "FeatureType":
        return FeatureType(name="string")

    @property
    def int32(self) -> "FeatureType":
        return FeatureType(name="int32")

    @property
    def bool(self) -> "FeatureType":
        return FeatureType(name="bool")

    @property
    def int64(self) -> "FeatureType":
        return FeatureType(name="int64")

    @property
    def float(self) -> "FeatureType":
        return FeatureType(name="float")

    @property
    def double(self) -> "FeatureType":
        return FeatureType(name="double")
    
    @property
    def date(self) -> "FeatureType":
        return FeatureType(name="date")

    @property
    def uuid(self) -> "FeatureType":
        return FeatureType(name="uuid")

    @property
    def datetime(self) -> "FeatureType":
        return FeatureType(name="datetime")

    @property
    def array(self) -> "FeatureType":
        return FeatureType(name="array")


@dataclass
class Feature(Codable):
    name: str
    dtype: FeatureType
    description: str | None = None
    tags: dict[str, str] | None = None

    constraints: set[Constraint] | None = None

    def __hash__(self) -> int:
        return hash(self.name)

@dataclass
class EventTimestamp(Codable):
    name: str
    ttl: int
    description: str | None = None
    tags: dict[str, str] | None = None
    dtype: FeatureType = FeatureType("").datetime

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class FeatureReferance(Codable):
    name: str
    feature_view: str
    dtype: FeatureType
    is_derivied: bool

    def __hash__(self) -> int:
        return hash(self.name)