import pytest

from pathlib import Path

from otherworld_asset_service.api.service import OtherWorldAssetService
from otherworld_asset_service.api.validation.pipelines.asset_pipeline import (
    build_default_asset_pipeline,
)
from otherworld_asset_service.api.validation.pipelines.asset_version_pipeline import (
    build_default_asset_version_pipeline,
)
from otherworld_asset_service.models.asset import Asset
from otherworld_asset_service.models.asset_version import AssetVersion
from otherworld_asset_service.models.enums import AssetType, VersionStatus
from otherworld_asset_service.storage.sqlite_database import SQLiteDatabase


ASSET_TYPE = AssetType.CHARACTER
CHARACTER_NAME = "coraline"
DEPARTMENT = "animation"
VERSION_STATUS = VersionStatus.ACTIVE


@pytest.fixture
def sqlite_database():
    """Test fixture to provide a SQLiteDatabase instance for each test run.

    The SQLiteDatabase safely closes when no longer in use.

    Yields:
        SQLiteDatabase: The newly created SQLiteDatabase instance to test with.
    """

    data_store = SQLiteDatabase()

    try:
        yield data_store
    finally:
        data_store.close()


@pytest.fixture
def asset_service(sqlite_database: SQLiteDatabase) -> OtherWorldAssetService:
    """Test fixture to provide an asset service instance for each test run.

    Args:
        sqlite_database (SQLiteDatabase): The sqlite database used for tests.

    Returns:
        OtherWorldAssetService: The service to execute tests on.
    """

    return OtherWorldAssetService(
        data_store=sqlite_database,
        asset_pipeline=build_default_asset_pipeline(),
        asset_version_pipeline=build_default_asset_version_pipeline(),
    )


def test_service_load_assets(asset_service: OtherWorldAssetService):
    tests_directory = Path(__file__).parent
    sample_data = tests_directory / "sample_data.json"

    assert asset_service.load_assets(file_path=sample_data) is None


def test_service_add_asset(asset_service: OtherWorldAssetService):
    assert asset_service.add_asset(Asset(CHARACTER_NAME, ASSET_TYPE))


def test_service_add_asset_version(asset_service: OtherWorldAssetService):
    asset = asset_service.add_asset(Asset(CHARACTER_NAME, ASSET_TYPE))
    asset_version = AssetVersion(asset.id, DEPARTMENT, 1, VERSION_STATUS)

    assert asset_service.add_asset_version(asset, asset_version)


def test_service_list_assets(asset_service: OtherWorldAssetService):
    assert len(asset_service.list_assets()) == 0

    asset_service.add_asset(Asset(CHARACTER_NAME, ASSET_TYPE))

    assert len(asset_service.list_assets()) == 1


def test_service_get_asset(asset_service: OtherWorldAssetService):
    asset = asset_service.add_asset(Asset(CHARACTER_NAME, ASSET_TYPE))

    assert asset_service.get_asset(asset.name)


def test_service_get_asset_version(asset_service: OtherWorldAssetService):
    asset = asset_service.add_asset(Asset(CHARACTER_NAME, ASSET_TYPE))
    asset_version = AssetVersion(asset.id, DEPARTMENT, 1, VERSION_STATUS)
    asset_service.add_asset_version(asset, asset_version)

    assert asset_service.get_asset_version(asset.name, 1)


def test_service_list_asset_versions(asset_service: OtherWorldAssetService):
    asset = asset_service.add_asset(Asset(CHARACTER_NAME, ASSET_TYPE))
    asset_version_v1 = AssetVersion(asset.id, DEPARTMENT, 1, VERSION_STATUS)
    asset_version_v2 = AssetVersion(asset.id, DEPARTMENT, 2, VERSION_STATUS)
    asset_version_v3 = AssetVersion(asset.id, DEPARTMENT, 3, VERSION_STATUS)

    asset_service.add_asset_version(asset, asset_version_v1)

    assert len(asset_service.list_asset_versions(asset.name)) == 1

    asset_service.add_asset_version(asset, asset_version_v2)

    assert len(asset_service.list_asset_versions(asset.name)) == 2

    asset_service.add_asset_version(asset, asset_version_v3)

    assert len(asset_service.list_asset_versions(asset.name)) == 3
