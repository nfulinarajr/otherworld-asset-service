from otherworld_asset_service.api.validation.errors import ValidationError
from otherworld_asset_service.models.enums import Department, VersionStatus
from otherworld_asset_service.models.version import Version


class VersionDepartmentIsRequiredRule:
    """Validation rule to ensure department exists."""

    def validate(self, version: Version) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        if not version.department:
            validation_errors.append(
                ValidationError(
                    field="department", message="Version must define a valid department"
                )
            )

        return validation_errors


class VersionDepartmentTypeIsCorrectRule:
    """Validation rule to ensure the department data type is correct."""

    def validate(self, version: Version) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        if not isinstance(version.department, Department):
            validation_errors.append(
                ValidationError(
                    field="department",
                    message="Version department must be of type Department",
                )
            )

        return validation_errors


class VersionNumberIsGreaterThanOneRule:
    """Rule to validate the version number is greater than or equal to 1."""

    def validate(self, version: Version) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        if version.number < 1:
            validation_errors.append(
                ValidationError(
                    field="number",
                    message="Version number must be greater than or equal to 1",
                )
            )

        return validation_errors


class VersionStatusIsKnownRule:
    """Validation rule to ensure version status exists."""

    def validate(self, version: Version) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        try:
            VersionStatus(version.status)
        except ValueError:
            validation_errors.append(
                ValidationError(
                    field="status",
                    message="Version status must match a known VersionStatus value",
                )
            )

        return validation_errors
