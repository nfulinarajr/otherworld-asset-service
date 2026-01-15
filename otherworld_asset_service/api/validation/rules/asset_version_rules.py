from otherworld_asset_service.api.validation.errors import ValidationError
from otherworld_asset_service.models.asset_version import AssetVersion
from otherworld_asset_service.models.enums import VersionStatus


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

        if not isinstance(asset_version.department, str):
            validation_errors.append(
                ValidationError(
                    field="department",
                    message="Asset version department must be of type str",
                )
            )

        return validation_errors


class AssetVersionIsGreaterThanOneRule:
    """Validation rule to ensure asset version is greater than or equal to 1."""

    def validate(self, asset_version: AssetVersion) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        if asset_version.version is not None and asset_version.version < 1:
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
            VersionStatus(asset_version.status)
        except ValueError:
            validation_errors.append(
                ValidationError(
                    field="status",
                    message="Asset version status must be of type VersionStatus",
                )
            )

        return validation_errors
