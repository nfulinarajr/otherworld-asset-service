import json
import sqlite3

from pathlib import Path
from typing import Optional

from otherworld_asset_service.models.asset import Asset
from otherworld_asset_service.models.asset_version import AssetVersion
from otherworld_asset_service.models.enums import AssetType, VersionStatus
from otherworld_asset_service.storage.sqlite_database import SQLiteDatabase
from otherworld_asset_service.utils import logger


LOGGER = logger.get_logger()


class OtherWorldAssetService:
    """The main API and entry point for interacting with assets and asset versions."""

    def __init__(self, data_store_path, asset_pipeline, asset_version_pipeline):
        self._data_store = SQLiteDatabase(data_store_path)
        self._asset_pipeline = asset_pipeline
        self._asset_version_pipeline = asset_version_pipeline

    def load_assets(self, file_path: str):
        """Load all assets from a file.

        NOTE: This method assumes a JSON file with a flat structure.

        Args:
            file_path (str): The JSON file path.
        """

        LOGGER.debug("Loading assets from {}".format(file_path))

        path = Path(file_path)
        json_data = json.loads(path.read_text())

        for asset_entry in json_data:
            # Parse asset data
            asset_data = asset_entry.get("asset")
            asset_name = asset_data.get("name")
            asset_type = asset_data.get("type")

            try:
                # Confirm the asset type exists
                asset_type = AssetType(asset_type)
            except ValueError as error:
                LOGGER.error(error)
                continue

            asset = self.add_asset(Asset(asset_name, asset_type))

            # Handle the scenario where the asset could not be added for reasons other
            # than already existing within the data store. If any errors occurred, check
            # if the asset already exists and if so, use that.
            asset = asset or self.get_asset(asset_name)

            if not asset:
                # Continue to the next entry since adding an asset must contain a name
                # and type
                continue

            # Parse asset version data
            version_department = asset_entry.get("department")
            version_number = asset_entry.get("version")
            version_status = asset_entry.get("status")

            try:
                # Confirm the status exists
                version_status = VersionStatus(version_status)
            except ValueError as error:
                LOGGER.error(error)
                continue

            self.add_asset_version(
                asset,
                AssetVersion(
                    asset.id,
                    version_department,
                    version=version_number,
                    status=version_status,
                ),
            )

    def add_asset(self, asset: Asset) -> Optional[Asset]:
        """Add an asset to the data store.

        Args:
            asset (str): The asset to add.

        Returns:
            Asset: The added asset.
        """

        LOGGER.debug(
            "Adding asset for {} ({})".format(asset.name, asset.asset_type.value)
        )

        validation_errors = self._asset_pipeline.validate(asset)

        if validation_errors:
            for error in validation_errors:
                LOGGER.error(error)
            return

        try:
            return self._data_store.add_asset(asset)
        except sqlite3.IntegrityError as error:
            LOGGER.error(error)

            # Catch the exception when adding an asset that is not unique. If not, check
            # if an asset exists that matches the same name and type.
            existing_asset = self._data_store.get_asset(asset.name)

            return existing_asset or None

    def add_asset_version(self, asset: Asset, version: AssetVersion) -> AssetVersion:
        """Add an asset version to the data store.

        Args:
            asset (Asset): The asset to be versioned.
            version (AssetVersion): The version data associated with the asset.

        Returns:
            AssetVersion: The added asset version.
        """

        LOGGER.debug(
            "Adding version for {} ({})".format(asset.name, asset.asset_type.value)
        )

        validation_errors = self._asset_pipeline.validate(asset)
        validation_errors.extend(self._asset_version_pipeline.validate(version))

        if validation_errors:
            for error in validation_errors:
                LOGGER.error(error)
            return

        try:
            if not version.version:
                latest_version = self._data_store.get_last_asset_version_number(
                    asset.id
                )

                if latest_version is None:
                    latest_version = 1
                else:
                    latest_version += 1

                version = AssetVersion(
                    asset.id,
                    version.department,
                    version=latest_version,
                    status=version.status,
                )

            return self._data_store.add_asset_version(
                asset=asset, asset_version=version
            )
        except sqlite3.IntegrityError as error:
            # Catch the exception when adding an asset version that is not unique
            LOGGER.error(error)

    def list_assets(self) -> list[Asset]:
        """List all assets within the data store.

        Returns:
            list[Asset]: A list of assets currently in the data store.
        """

        LOGGER.debug("Listing all assets")

        return self._data_store.list_assets()

    def get_asset(self, asset_name: str) -> Asset:
        """Get an asset from the data store.

        Args:
            asset_name (str): The asset to get.

        Returns:
            Asset: The asset found matching the provided asset name.
        """

        LOGGER.debug("Getting asset for {}".format(asset_name))

        return self._data_store.get_asset(asset_name)

    def get_asset_version(self, asset_name: str, version: int) -> AssetVersion:
        """Get an asset version from the data store.

        Args:
            asset_name (str): The asset name necessary for version lookup.
            version (int): The version number to find.

        Returns:
            AssetVersion: The asset version found matching the provided name and number.
        """

        LOGGER.debug("Getting asset version for {}".format(asset_name))

        # Get the asset from the data store to ensure data is current
        asset = self._data_store.get_asset(name=asset_name)

        # Use the asset id to get the specific asset version
        return self._data_store.get_asset_version(asset_id=asset.id, version=version)

    def list_asset_versions(self, asset_name: str) -> list[AssetVersion]:
        """List all assets versions for an asset.

        Args:
            asset_name (str): The asset name used to find all versions for an asset.

        Returns:
            list[AssetVersion]: A list of versions.
        """

        LOGGER.debug("Listing all asset versions for {}".format(asset_name))

        # Get the asset from the data store to ensure data is correct
        asset = self._data_store.get_asset(name=asset_name)

        # Use the asset id to get all asset versions
        return self._data_store.list_asset_versions(asset_id=asset.id)
