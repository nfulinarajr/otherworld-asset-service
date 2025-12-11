import pytest

from otherworld_asset_service.models.enums import AssetType, Department, Status


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
    # Verify asset version status usage when value does not exist
    with pytest.raises(ValueError):
        Status(INVALID_VALUE)
