import pytest

from aladdin import FeatureStore, FeatureView


@pytest.mark.asyncio
async def test_all_features(
    breast_scan_without_timestamp_feature_store: FeatureStore,
    breast_scan_feature_viewout_with_datetime: FeatureView,
) -> None:
    store = breast_scan_without_timestamp_feature_store
    feature_view = breast_scan_feature_viewout_with_datetime

    features = await store.feature_view(feature_view.metadata.name).all().to_df()

    for feature in type(breast_scan_feature_viewout_with_datetime).select_all().features_to_include:
        assert feature in features.columns

    assert 'is_malignant' in features.columns
    assert not features['is_malignant'].isna().any()
    assert 'diagnosis' in features.columns
    assert 'scan_id' in features.columns

    limit = 10
    limit_features = await store.feature_view(feature_view.metadata.name).all(limit=limit).to_df()

    assert limit_features.shape[0] == limit
