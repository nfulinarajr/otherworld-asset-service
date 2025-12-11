from otherworld_asset_service.api.validation.rules.asset_rules import (
    AssetNameIsRequiredRule,
    AssetNameIsValidRule,
    AssetTypeIsRequiredRule,
    AssetTypeIsValidRule,
)
from otherworld_asset_service.api.validation.validation import ValidationPipeline
from otherworld_asset_service.models.asset import Asset


def build_default_asset_pipeline() -> ValidationPipeline[Asset]:
    """Build a default asset validation pipeline.

    Returns:
        ValidationPipeline[Asset]: A collection of all asset validation rules.
    """

    return ValidationPipeline[Asset](
        rules=[
            AssetNameIsRequiredRule(),
            AssetNameIsValidRule(),
            AssetTypeIsRequiredRule(),
            AssetTypeIsValidRule(),
        ]
    )
