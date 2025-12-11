import pytest

from otherworld_asset_service.models.asset import Asset
from otherworld_asset_service.models.enums import AssetType


ASSET_NAME = "Coraline"


def test_asset_creation_with_required_values():
    # Create asset with valid name and type
    asset = Asset(name=ASSET_NAME, type=AssetType.CHARACTER)

    # Verify the asset name is correctly stored
    assert asset.name == ASSET_NAME

    # Verify the asset type is correctly stored
    assert asset.type == AssetType.CHARACTER


def test_asset_creation_with_missing_name():
    # Create asset with missing name
    with pytest.raises(TypeError):
        Asset(type=AssetType.CHARACTER)


def test_asset_creation_with_missing_type():
    # Create asset with missing type
    with pytest.raises(TypeError):
        Asset(name=ASSET_NAME)
