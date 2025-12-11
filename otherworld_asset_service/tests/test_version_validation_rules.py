from otherworld_asset_service.api.validation.rules.asset_version_rules import (
    AssetVersionDepartmentIsRequiredRule,
    AssetVersionDepartmentIsValidRule,
    AssetVersionIsGreaterThanOneRule,
    AssetVersionStatusIsKnownRule,
)
from otherworld_asset_service.models.enums import Department
from otherworld_asset_service.models.asset_version import AssetVersion


def test_asset_version_department_is_required_rule():
    # Create the asset version
    asset_version = AssetVersion(asset=1, department=Department.ANIMATION)

    # Create the validation rule
    rule = AssetVersionDepartmentIsRequiredRule()

    # Validate the asset version
    validation_errors = rule.validate(asset_version)

    assert validation_errors == []

    # Update asset version department to a None type
    asset_version.department = None

    # Validate the asset version
    validation_errors = rule.validate(asset_version)

    # Verify the single validation error exists for the department field
    assert len(validation_errors) == 1
    assert validation_errors[0].field == "department"


def test_asset_version_department_is_correct_type_rule():
    # Create the asset version
    asset_version = AssetVersion(asset=1, department=Department.ANIMATION)

    # Create the validation rule
    rule = AssetVersionDepartmentIsValidRule()

    # Validate the asset version
    validation_errors = rule.validate(asset_version)

    assert validation_errors == []

    # Update asset version department to an invalid type
    asset_version.department = "Foo"

    # Validate the asset version
    validation_errors = rule.validate(asset_version)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "department"


def test_asset_version_is_greater_than_one_rule():
    # Create the asset version
    asset_version = AssetVersion(asset=1, department=Department.ANIMATION, version=1)

    # Create the validation rule
    rule = AssetVersionIsGreaterThanOneRule()

    # Validate the asset version
    validation_errors = rule.validate(asset_version)

    assert validation_errors == []

    # Update asset version to be below 1
    asset_version.version = 0

    # Validate the version
    validation_errors = rule.validate(asset_version)

    # Verify the single validation error exists for the version field
    assert len(validation_errors) == 1
    assert validation_errors[0].field == "version"


def test_asset_version_status_is_known_rule():
    # Create the asset version
    asset_version = AssetVersion(asset=1, department=Department.ANIMATION)

    # Create the validation rule
    rule = AssetVersionStatusIsKnownRule()

    # Validate the asset version
    validation_errors = rule.validate(asset_version)

    assert validation_errors == []

    # Update asset version status to an invalid type
    asset_version.status = "Foo"

    # Validate the asset version
    validation_errors = rule.validate(asset_version)

    # Verify the single validation error exists for the status field
    assert len(validation_errors) == 1
    assert validation_errors[0].field == "status"
