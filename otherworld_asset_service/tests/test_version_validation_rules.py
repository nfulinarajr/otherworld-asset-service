from otherworld_asset_service.api.validation.rules.asset_version_rules import (
    AssetVersionDepartmentIsRequiredRule,
    AssetVersionDepartmentIsValidRule,
    AssetVersionIsGreaterThanOneRule,
    AssetVersionStatusIsKnownRule,
)
from otherworld_asset_service.models.asset_version import AssetVersion


DEPARTMENT = "animation"


def test_asset_version_department_is_required_rule():
    asset_version = AssetVersion(asset=1, department=DEPARTMENT)

    rule = AssetVersionDepartmentIsRequiredRule()

    validation_errors = rule.validate(asset_version)

    assert validation_errors == []

    asset_version.department = None

    validation_errors = rule.validate(asset_version)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "department"


def test_asset_version_department_is_correct_type_rule():
    asset_version = AssetVersion(asset=1, department=DEPARTMENT)

    rule = AssetVersionDepartmentIsValidRule()

    validation_errors = rule.validate(asset_version)

    assert validation_errors == []

    asset_version.department = 1

    validation_errors = rule.validate(asset_version)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "department"


def test_asset_version_is_greater_than_one_rule():
    asset_version = AssetVersion(asset=1, department=DEPARTMENT, version=1)

    rule = AssetVersionIsGreaterThanOneRule()

    validation_errors = rule.validate(asset_version)

    assert validation_errors == []

    asset_version.version = 0

    validation_errors = rule.validate(asset_version)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "version"


def test_asset_version_status_is_known_rule():
    asset_version = AssetVersion(asset=1, department=DEPARTMENT)

    rule = AssetVersionStatusIsKnownRule()

    validation_errors = rule.validate(asset_version)

    assert validation_errors == []

    asset_version.status = "Foo"

    validation_errors = rule.validate(asset_version)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "status"
