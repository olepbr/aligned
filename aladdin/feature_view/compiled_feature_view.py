from dataclasses import dataclass
from aladdin.derivied_feature import DerivedFeature

from aladdin.feature import Feature
from aladdin.data_source.batch_data_source import BatchDataSource
from aladdin.data_source.stream_data_source import StreamDataSource
from aladdin.request.retrival_request import RetrivalRequest
from aladdin.codable import Codable

@dataclass
class CompiledFeatureView(Codable):
    name: str
    description: str
    tags: dict[str, str]
    batch_data_source: BatchDataSource
    # stream_data_source: StreamDataSource | None

    entities: set[Feature]
    features: set[Feature]
    derived_features: set[DerivedFeature]


    @property
    def entitiy_names(self) -> set[str]:
        return {entity.name for entity in self.entities}

    
    @property
    def request_all(self) -> RetrivalRequest:
        return RetrivalRequest(
            feature_view_name=self.name,
            entities=self.entities,
            features=self.features,
            derived_features=self.derived_features
        )

    def request_for(self, feature_names: set[str]) -> RetrivalRequest:
        return RetrivalRequest(
            feature_view_name=self.name,
            entities=self.entities,
            features={feature for feature in self.features if feature.name in feature_names},
            derived_features={feature for feature in self.derived_features if feature.name in feature_names}
        )

    def __hash__(self) -> int:
        return hash(self.name)

    # @classmethod
    # def __post_deserialize__(cls, obj: "CompiledFeatureView") -> "CompiledFeatureView":
    #     obj.entities = set(obj.entities)
    #     obj.features = set(obj.features)
    #     obj.derived_features = set(obj.derived_features)
    #     return obj