from otherworld_asset_service.api.validation.pipelines.asset_pipeline import (
    build_default_asset_pipeline,
)
from otherworld_asset_service.api.validation.pipelines.version_pipeline import (
    build_default_version_pipeline,
)
from otherworld_asset_service.models.asset import Asset
from otherworld_asset_service.models.enums import AssetType, Department
from otherworld_asset_service.models.version import Version


ASSET_NAME = "Coraline"


def test_build_default_asset_pipeline():
    # Build the default asset pipeline
    pipeline = build_default_asset_pipeline()

    # Ensure pipeline contains four default rules
    assert len(pipeline.rules) == 4

    # Create asset
    asset = Asset(name=ASSET_NAME, type=AssetType.CHARACTER)

    # Execute pipeline validation
    validation_errors = pipeline.validate(asset)

    assert validation_errors == []

    # Update two properties to be invalid
    asset.name = None
    asset.type = 1

    # Execute pipeline validation
    validation_errors = pipeline.validate(asset)

    # Three errors are expected since the absence of an asset name returns two errors
    # including the single error for the asset type being incorrect
    assert len(validation_errors) == 3

    # Verify the name and type fields are contained within the validation errors
    fields = [error.field for error in validation_errors]
    assert "name" in fields
    assert "type" in fields

    # Confirm the three validation errors returned consists of two name fields and one
    # type field
    assert fields.count("name") == 2
    assert fields.count("type") == 1


def test_build_default_version_pipeline():
    # Build the default version pipeline
    pipeline = build_default_version_pipeline()

    # Ensure pipeline contains four default rules
    assert len(pipeline.rules) == 4

    # Create version
    version = Version(asset_id=1, department=Department.ANIMATION)

    # Execute pipeline validation
    validation_errors = pipeline.validate(version)

    assert validation_errors == []

    # Update two properties to be invalid
    version.number = 0
    version.department = "Foo"

    # Execute pipeline validation
    validation_errors = pipeline.validate(version)

    # Two errors are expected to reflect each updated property
    assert len(validation_errors) == 2

    # Verify the department and number fields are contained within the validation errors
    fields = [error.field for error in validation_errors]
    assert "department" in fields
    assert "number" in fields

    # Confirm the two validation errors returned consists of one department field and
    # one number field
    assert fields.count("department") == 1
    assert fields.count("number") == 1
