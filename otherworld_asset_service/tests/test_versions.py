import pytest

from otherworld_asset_service.models.enums import Department, Status
from otherworld_asset_service.models.asset_version import AssetVersion


def test_version_creation_with_required_and_default_values():
    # Create asset version with valid asset id, department, default version, and
    # default asset version status values
    asset_version = AssetVersion(asset=1, department=Department.ANIMATION)

    # Verify the asset version is correctly stored
    assert asset_version.asset == 1

    # Verify the department is correctly stored
    assert asset_version.department == Department.ANIMATION

    # Verify the default asset version is valid
    assert asset_version.version == 1

    # Verify the default asset version status is valid
    assert asset_version.status == Status.INACTIVE


def test_asset_version_creation_with_missing_asset():
    # Create version with missing asset
    with pytest.raises(TypeError):
        AssetVersion(department=Department.ANIMATION)


def test_asset_version_creation_with_missing_department():
    # Create asset version with missing department
    with pytest.raises(TypeError):
        AssetVersion(asset=1)


def test_asset_version_creation_with_invalid_asset_version():
    # Create asset version with invalid version
    with pytest.raises(ValueError):
        AssetVersion(asset=1, department=Department.ANIMATION, version=0)
