from otherworld_asset_service.api.validation.rules.asset_rules import (
    AssetNameIsRequiredRule,
    AssetNameIsValidRule,
    AssetTypeIsRequiredRule,
    AssetTypeIsValidRule,
)
from otherworld_asset_service.models.asset import Asset
from otherworld_asset_service.models.enums import AssetType


ASSET_NAME = "Coraline"


def test_asset_name_is_required_rule():
    # Create the asset
    asset = Asset(name=ASSET_NAME, type=AssetType.CHARACTER)

    # Create the validation rule
    rule = AssetNameIsRequiredRule()

    # Validate the asset
    validation_errors = rule.validate(asset)

    assert validation_errors == []

    # Update asset name to a None type
    asset.name = None

    # Validate the asset
    validation_errors = rule.validate(asset)

    # Verify the single validation error exists for the name field
    assert len(validation_errors) == 1
    assert validation_errors[0].field == "name"


def test_asset_name_is_correct_type_rule():
    # Create the asset
    asset = Asset(name=ASSET_NAME, type=AssetType.CHARACTER)

    # Create the validation rule
    rule = AssetNameIsValidRule()

    # Validate the asset
    validation_errors = rule.validate(asset)

    assert validation_errors == []

    # Update asset name to an invalid type
    asset.name = 1

    # Validate the asset
    validation_errors = rule.validate(asset)

    # Verify the single validation error exists for the name field
    assert len(validation_errors) == 1
    assert validation_errors[0].field == "name"


def test_asset_type_is_required_rule():
    # Create the asset
    asset = Asset(name=ASSET_NAME, type=AssetType.CHARACTER)

    # Create the validation rule
    rule = AssetTypeIsRequiredRule()

    # Validate the asset
    validation_errors = rule.validate(asset)

    assert validation_errors == []

    # Update asset type to a None type
    asset.type = None

    # Validate the asset
    validation_errors = rule.validate(asset)

    # Verify the single validation error exists for the type field
    assert len(validation_errors) == 1
    assert validation_errors[0].field == "type"


def test_asset_type_is_correct_type_rule():
    # Create the asset
    asset = Asset(name=ASSET_NAME, type=AssetType.CHARACTER)

    # Create the validation rule
    rule = AssetTypeIsValidRule()

    # Validate the asset
    validation_errors = rule.validate(asset)

    assert validation_errors == []

    # Update asset type to an invalid type
    asset.type = 1

    # Validate the asset
    validation_errors = rule.validate(asset)

    # Verify the single validation error exists for the type field
    assert len(validation_errors) == 1
    assert validation_errors[0].field == "type"
