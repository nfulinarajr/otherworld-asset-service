import pytest

from otherworld_asset_service.models.enums import VersionStatus
from otherworld_asset_service.models.asset_version import AssetVersion


DEPARTMENT = "animation"


def test_version_creation_with_required_and_default_values():
    asset_version = AssetVersion(asset=1, department=DEPARTMENT)

    assert asset_version.asset == 1
    assert asset_version.department == DEPARTMENT
    assert asset_version.version == 1
    assert asset_version.status == VersionStatus.INACTIVE


def test_asset_version_creation_with_missing_asset():
    with pytest.raises(TypeError):
        AssetVersion(department=DEPARTMENT)


def test_asset_version_creation_with_missing_department():
    with pytest.raises(TypeError):
        AssetVersion(asset=1)


def test_asset_version_creation_with_invalid_asset_version():
    # Handling validation through the pipelines as opposed to the object itself
    pass
