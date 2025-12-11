from otherworld_asset_service.api.validation.errors import ValidationError
from otherworld_asset_service.models.enums import Department, Status
from otherworld_asset_service.models.asset_version import AssetVersion


class AssetVersionDepartmentIsRequiredRule:
    """Validation rule to ensure department exists."""

    def validate(self, asset_version: AssetVersion) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        if not asset_version.department:
            validation_errors.append(
                ValidationError(
                    field="department",
                    message="Asset version must define a valid department",
                )
            )

        return validation_errors


class AssetVersionDepartmentIsValidRule:
    """Validation rule to ensure the department data type is valid."""

    def validate(self, asset_version: AssetVersion) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        if not isinstance(asset_version.department, Department):
            validation_errors.append(
                ValidationError(
                    field="department",
                    message="Asset version department must be of type Department",
                )
            )

        return validation_errors


class AssetVersionIsGreaterThanOneRule:
    """Rule to validate the asset version to be greater than or equal to 1."""

    def validate(self, asset_version: AssetVersion) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        if asset_version.version < 1:
            validation_errors.append(
                ValidationError(
                    field="version",
                    message="Asset version must be greater than or equal to 1",
                )
            )

        return validation_errors


class AssetVersionStatusIsKnownRule:
    """Validation rule to ensure asset version status exists."""

    def validate(self, asset_version: AssetVersion) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        try:
            Status(asset_version.status)
        except ValueError:
            validation_errors.append(
                ValidationError(
                    field="status",
                    message="Asset version status must be of type Status",
                )
            )

        return validation_errors
