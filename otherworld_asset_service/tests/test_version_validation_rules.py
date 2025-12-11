from otherworld_asset_service.api.validation.rules.version_rules import (
    VersionDepartmentIsRequiredRule,
    VersionDepartmentTypeIsCorrectRule,
    VersionNumberIsGreaterThanOneRule,
    VersionStatusIsKnownRule,
)
from otherworld_asset_service.models.enums import Department
from otherworld_asset_service.models.version import Version


def test_version_department_is_required_rule():
    # Create the version
    version = Version(asset_id=1, department=Department.ANIMATION)

    # Create the validation rule
    rule = VersionDepartmentIsRequiredRule()

    # Validate the version
    validation_errors = rule.validate(version)

    assert validation_errors == []

    # Update version department to a None type
    version.department = None

    # Validate the version
    validation_errors = rule.validate(version)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "department"


def test_version_department_is_correct_type_rule():
    # Create the version
    version = Version(asset_id=1, department=Department.ANIMATION)

    # Create the validation rule
    rule = VersionDepartmentTypeIsCorrectRule()

    # Validate the version
    validation_errors = rule.validate(version)

    assert validation_errors == []

    # Update version department to an invalid type
    version.department = "Foo"

    # Validate the version
    validation_errors = rule.validate(version)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "department"


def test_version_number_is_greater_than_one_rule():
    # Create the version
    version = Version(asset_id=1, department=Department.ANIMATION, number=1)

    # Create the validation rule
    rule = VersionNumberIsGreaterThanOneRule()

    # Validate the version
    validation_errors = rule.validate(version)

    assert validation_errors == []

    # Update version number below 1
    version.number = 0

    # Validate the version
    validation_errors = rule.validate(version)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "number"


def test_version_status_is_known_rule():
    # Create the version
    version = Version(asset_id=1, department=Department.ANIMATION)

    # Create the validation rule
    rule = VersionStatusIsKnownRule()

    # Validate the version
    validation_errors = rule.validate(version)

    assert validation_errors == []

    # Update version status to an invalid type
    version.status = "Foo"

    # Validate the version
    validation_errors = rule.validate(version)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "status"
