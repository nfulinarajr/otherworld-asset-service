from otherworld_asset_service.api.validation.rules.version_rules import (
    VersionDepartmentIsRequiredRule,
    VersionDepartmentTypeIsCorrectRule,
    VersionNumberIsGreaterThanOneRule,
    VersionStatusIsKnownRule,
)
from otherworld_asset_service.api.validation.validation import ValidationPipeline
from otherworld_asset_service.models.version import Version


def build_default_version_pipeline() -> ValidationPipeline[Version]:
    """Build a default version validation pipeline.

    Returns:
        ValidationPipeline[Version]: A collection of all version validation rules.
    """

    return ValidationPipeline[Version](
        rules=[
            VersionDepartmentIsRequiredRule(),
            VersionDepartmentTypeIsCorrectRule(),
            VersionNumberIsGreaterThanOneRule(),
            VersionStatusIsKnownRule(),
        ]
    )
