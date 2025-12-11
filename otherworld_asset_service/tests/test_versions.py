import pytest

from otherworld_asset_service.models.version import Version
from otherworld_asset_service.models.enums import Department
from otherworld_asset_service.models.enums import VersionStatus


def test_version_creation_with_required_and_default_values():
    # Create version with valid asset id, department, default version number, and
    # default version status values
    version = Version(asset_id=1, department=Department.ANIMATION)

    # Verify the version number is correctly stored
    assert version.asset_id == 1

    # Verify the department is correctly stored
    assert version.department == Department.ANIMATION

    # Verify the default version number is valid
    assert version.number == 1

    # Verify the default version status is valid
    assert version.status == VersionStatus.INACTIVE


def test_version_creation_with_missing_asset_id():
    # Create version with missing asset id
    with pytest.raises(TypeError):
        Version(department=Department.ANIMATION)


def test_version_creation_with_missing_department():
    # Create version with missing department
    with pytest.raises(TypeError):
        Version(asset_id=1)


def test_version_creation_with_invalid_version_number():
    # Create version with invalid version number
    with pytest.raises(ValueError):
        Version(asset_id=1, department=Department.ANIMATION, number=0)
