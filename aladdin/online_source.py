from dataclasses import dataclass
from abc import ABC, abstractmethod
from aladdin.codable import Codable
from aladdin.feature_source import FeatureSource
from aladdin.feature_view.compiled_feature_view import CompiledFeatureView
from mashumaro.types import SerializableType
from typing import Optional

class OnlineSourceFactory:

    supported_sources: dict[str, type["OnlineSource"]]

    _shared: Optional["OnlineSourceFactory"] = None

    def __init__(self):
        from aladdin.redis.config import RedisOnlineSource
        self.supported_sources = {
            BatchOnlineSource.source_type: BatchOnlineSource,
            RedisOnlineSource.source_type: RedisOnlineSource
        }

    @classmethod
    def shared(cls) -> "OnlineSourceFactory":
        if cls._shared:
            return cls._shared
        cls._shared = OnlineSourceFactory()
        return cls._shared


class OnlineSource(ABC, Codable, SerializableType):
    """
    A codable source, that can create a feature source.

    This is sepearted form the FeatureSource, as this may contain additional information that should not be decoded.
    """

    source_type: str

    @abstractmethod
    def feature_source(self, feature_views: set[CompiledFeatureView]) -> FeatureSource:
        pass

    def _serialize(self):
        return self.to_dict()

    def __hash__(self) -> int:
        return hash(self.source_type)

    @classmethod
    def _deserialize(cls, value: dict[str]) -> 'OnlineSource':
        try:
            name_type = value["source_type"]

            if name_type not in OnlineSourceFactory.shared().supported_sources:
                raise ValueError(f"Unknown online source id: '{name_type}'.\nRemember to add the data source to the 'OnlineSourceFactory.supported_sources' if it is a custom type.")
            del value["source_type"]

            data_class = OnlineSourceFactory.shared().supported_sources[name_type]

            return data_class.from_dict(value)
        except Exception as error:
            print(error)


@dataclass
class BatchOnlineSource(OnlineSource):

    source_type = "batch"

    def feature_source(self, feature_views: set[CompiledFeatureView]) -> FeatureSource:
        from aladdin.job_factories import get_factories
        from aladdin.feature_source import BatchFeatureSource
        return BatchFeatureSource(
            get_factories(),
            sources={fv.name: fv.batch_data_source for fv in feature_views}
        )