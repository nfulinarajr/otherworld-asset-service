from otherworld_asset_service.api.validation.rules.asset_version_rules import (
    AssetVersionDepartmentIsRequiredRule,
    AssetVersionDepartmentIsValidRule,
    AssetVersionIsGreaterThanOneRule,
    AssetVersionStatusIsKnownRule,
)
from otherworld_asset_service.api.validation.validation import ValidationPipeline
from otherworld_asset_service.models.asset_version import AssetVersion


def build_default_asset_version_pipeline() -> ValidationPipeline[AssetVersion]:
    """Build a default asset version validation pipeline.

    Returns:
        ValidationPipeline[AssetVersion]: A collection of all asset version validation
            rules.
    """

    return ValidationPipeline[AssetVersion](
        rules=[
            AssetVersionDepartmentIsRequiredRule(),
            AssetVersionDepartmentIsValidRule(),
            AssetVersionIsGreaterThanOneRule(),
            AssetVersionStatusIsKnownRule(),
        ]
    )
