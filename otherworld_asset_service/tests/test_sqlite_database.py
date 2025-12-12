import pytest
import sqlite3

from otherworld_asset_service.models.asset import Asset
from otherworld_asset_service.models.asset_version import AssetVersion
from otherworld_asset_service.models.enums import AssetType, VersionStatus
from otherworld_asset_service.storage.sqlite_database import SQLiteDatabase


CHARACTER_NAME = "coraline"
DEPARTMENT = "animation"


@pytest.fixture
def sqlite_database():
    """Text fixture to provide a SQLiteDatabase instance for each test run.

    The SQLiteDatabase safely closes when no longer in use.

    Yields:
        SQLiteDatabase: The newly created SQLiteDatabase instance to test with.
    """

    database = SQLiteDatabase()

    try:
        yield database
    finally:
        database.close()


def test_empty_database(sqlite_database: SQLiteDatabase):
    assets = sqlite_database.list_assets()

    assert assets == []


def test_add_asset(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    added_asset = sqlite_database.add_asset(asset)

    assert added_asset.id is not None
    assert added_asset.name == CHARACTER_NAME
    assert added_asset.asset_type == AssetType.CHARACTER


def test_add_asset_version(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    added_asset = sqlite_database.add_asset(asset)

    asset_version = AssetVersion(
        asset=added_asset.id,
        department=DEPARTMENT,
        version=1,
        status=VersionStatus.ACTIVE,
    )
    added_asset_version = sqlite_database.add_asset_version(
        asset=added_asset, asset_version=asset_version
    )

    assert added_asset_version is not None
    assert added_asset_version.asset == added_asset.id
    assert added_asset_version.department == DEPARTMENT
    assert added_asset_version.version == 1
    assert added_asset_version.status == VersionStatus.ACTIVE


def test_add_asset_version_without_asset_id(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)

    asset_version = AssetVersion(
        asset=asset.id,
        department=DEPARTMENT,
        version=1,
        status=VersionStatus.ACTIVE,
    )

    # Attempt to add the version to the database. The expectation is a thrown exception
    # due to the asset not yet persisting.
    with pytest.raises(ValueError):
        sqlite_database.add_asset_version(asset=asset, asset_version=asset_version)


def test_get_asset(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    sqlite_database.add_asset(asset)

    found_asset = sqlite_database.get_asset(name=CHARACTER_NAME)

    assert found_asset is not None


def test_get_asset_does_not_exist(sqlite_database: SQLiteDatabase):
    assert not sqlite_database.get_asset(name="DoesNotExist")


def test_get_asset_version(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    added_asset = sqlite_database.add_asset(asset)

    asset_version_v1 = AssetVersion(
        asset=added_asset.id,
        department=DEPARTMENT,
        version=1,
        status=VersionStatus.INACTIVE,
    )
    sqlite_database.add_asset_version(asset=added_asset, asset_version=asset_version_v1)

    asset_version_v2 = AssetVersion(
        asset=added_asset.id,
        department=DEPARTMENT,
        version=2,
        status=VersionStatus.ACTIVE,
    )
    sqlite_database.add_asset_version(asset=added_asset, asset_version=asset_version_v2)

    found_asset = sqlite_database.get_asset_version(asset_id=added_asset.id, version=2)

    assert found_asset is not None
    assert found_asset.department == DEPARTMENT
    assert found_asset.version == 2
    assert found_asset.status == VersionStatus.ACTIVE


def test_list_assets(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    added_asset = sqlite_database.add_asset(asset)

    asset_version_v1 = AssetVersion(
        asset=added_asset.id,
        department=DEPARTMENT,
        version=1,
        status=VersionStatus.INACTIVE,
    )
    sqlite_database.add_asset_version(asset=added_asset, asset_version=asset_version_v1)

    all_assets = sqlite_database.list_assets()

    assert len(all_assets) == 1


def test_list_asset_versions(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    added_asset = sqlite_database.add_asset(asset)

    asset_version_v1 = AssetVersion(
        asset=added_asset.id,
        department=DEPARTMENT,
        version=1,
        status=VersionStatus.INACTIVE,
    )
    sqlite_database.add_asset_version(asset=added_asset, asset_version=asset_version_v1)

    asset_version_v2 = AssetVersion(
        asset=added_asset.id,
        department=DEPARTMENT,
        version=2,
        status=VersionStatus.ACTIVE,
    )
    sqlite_database.add_asset_version(asset=added_asset, asset_version=asset_version_v2)

    another_asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.PROP)
    another_added_asset = sqlite_database.add_asset(another_asset)

    another_asset_version_v1 = AssetVersion(
        asset=another_added_asset.id,
        department=DEPARTMENT,
        version=1,
        status=VersionStatus.INACTIVE,
    )
    sqlite_database.add_asset_version(
        asset=another_added_asset, asset_version=another_asset_version_v1
    )

    all_asset_versions = sqlite_database.list_asset_versions(asset_id=added_asset.id)

    assert len(all_asset_versions) == 2


def test_duplicate_assets(sqlite_database: SQLiteDatabase):
    original_asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    duplicated_asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)

    sqlite_database.add_asset(original_asset)

    # Attempt to add the duplicate asset to the database. The expectation is a thrown
    # exception due to asset name and type defining uniqueness.
    with pytest.raises(sqlite3.IntegrityError):
        sqlite_database.add_asset(duplicated_asset)


def test_duplicate_asset_versions(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    sqlite_database.add_asset(asset=asset)

    asset_version_v1 = AssetVersion(
        asset=asset.id,
        department=DEPARTMENT,
        version=1,
        status=VersionStatus.ACTIVE,
    )

    asset_version_v2 = AssetVersion(
        asset=asset.id,
        department=DEPARTMENT,
        version=1,
        status=VersionStatus.ACTIVE,
    )

    sqlite_database.add_asset_version(asset=asset, asset_version=asset_version_v1)

    # Attempt to add the duplicate asset to the database. The expectation is a thrown
    # exception due to asset id, department, and version number defining uniqueness.
    with pytest.raises(sqlite3.IntegrityError):
        sqlite_database.add_asset_version(asset=asset, asset_version=asset_version_v2)
