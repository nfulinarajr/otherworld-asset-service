import pytest

from otherworld_asset_service.models.enums import AssetType
from otherworld_asset_service.models.enums import Department
from otherworld_asset_service.models.enums import VersionStatus


INVALID_VALUE = "Foo"


def test_invalid_asset_type_value():
    # Verify asset type usage when value does not exist
    with pytest.raises(ValueError):
        AssetType(INVALID_VALUE)


def test_invalid_department_value():
    # Verify department usage when value does not exist
    with pytest.raises(ValueError):
        Department(INVALID_VALUE)


def test_invalid_version_status_value():
    # Verify version status usage when value does not exist
    with pytest.raises(ValueError):
        VersionStatus(INVALID_VALUE)
