import sqlite3

from otherworld_asset_service.models.asset import Asset
from otherworld_asset_service.models.asset_version import AssetVersion
from otherworld_asset_service.models.enums import AssetType, VersionStatus
from otherworld_asset_service.utils import logger


LOGGER = logger.get_logger("SQLiteDatabase")


class SQLiteDatabase:
    """A SQLite persistence layer to store asset and asset version data.

    Args:
        path (str): The location of the data store. If one is not provided, an in-memory
            SQLite database will be created instead.
    """

    def __init__(self, path: str = ":memory:") -> None:
        # Open a connection to the SQLite database using the provided path
        self._connection = sqlite3.connect(path)

        # Update the connection so queried rows will behave more like dicts than tuples
        self._connection.row_factory = sqlite3.Row

        # Initialize the schema
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        LOGGER.debug("Initializing database schema")

        cursor = self._connection.cursor()

        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS assets (
                asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                UNIQUE(name, type)
            );

            CREATE TABLE IF NOT EXISTS asset_versions (
                asset_id INTEGER NOT NULL,
                department TEXT NOT NULL,
                version INTEGER NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY(asset_id) REFERENCES assets(asset_id),
                UNIQUE(asset_id, department, version)
            );
            """
        )

        self._connection.commit()

    def add_asset(self, asset: Asset) -> Asset:
        """Add an asset to the database.

        Args:
            asset (Asset): The asset to add.

        Returns:
            Asset: The newly added asset.
        """

        LOGGER.debug("Adding asset for {}".format(asset.name))

        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO assets (name, type) VALUES (?, ?)",
            (asset.name, asset.asset_type.value),
        )

        self._connection.commit()

        # Update the asset now that it has a reference id
        asset.id = cursor.lastrowid

        LOGGER.debug("{} has been added!".format(asset.name))

        return asset

    def add_asset_version(
        self, asset: Asset, asset_version: AssetVersion
    ) -> AssetVersion:
        """Add an asset version to the database.

        Args:
            asset (Asset): The asset to reference.
            asset_version (AssetVersion): The asset version to add.

        Returns:
            AssetVersion: The newly added asset version.
        """

        LOGGER.debug("Adding asset version for {}".format(asset.name))

        if asset.id is None:
            raise ValueError("Asset versions must be associated with a valid asset id.")

        cursor = self._connection.cursor()

        cursor.execute(
            """
            INSERT INTO
            asset_versions (asset_id, department, version, status)
            VALUES (?, ?, ?, ?)
            """,
            (
                asset.id,
                asset_version.department,
                asset_version.version,
                asset_version.status.value,
            ),
        )

        self._connection.commit()

        LOGGER.debug("{} has been added!".format(asset.name))

        return AssetVersion(
            asset=asset.id,
            department=asset_version.department,
            version=asset_version.version,
            status=asset_version.status,
        )

    def get_asset(self, name: str) -> Asset | None:
        """Get the asset corresponding to the provided asset name.

        Args:
            name (str): The name of the asset to get.

        Returns:
            Asset | None: The asset corresponding to the provided asset name, or None if
                not found.
        """

        LOGGER.debug("Getting asset for {}".format(name))

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM assets WHERE name = ?",
            (name,),
        )

        row = cursor.fetchone()

        if not row:
            return None

        return Asset(
            id=row["asset_id"],
            name=row["name"],
            asset_type=AssetType(row["type"]),
        )

    def get_asset_version(self, asset_id: int, version: int) -> AssetVersion | None:
        """Get the asset version corresponding to the provided asset id.

        Args:
            asset_id (int): The asset id necessary to retrieve all associated versions.
            version (int): The specific version to get.

        Returns:
            AssetVersion | None: The asset version corresponding to the provided asset
            id, or None if not found.
        """

        LOGGER.debug("Getting asset version for {}".format(asset_id))

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM asset_versions WHERE asset_id = ? AND version = ?",
            (asset_id, version),
        )

        row = cursor.fetchone()

        if not row:
            return None

        return AssetVersion(
            asset=asset_id,
            department=row["department"],
            version=row["version"],
            status=VersionStatus(row["status"]),
        )

    def list_assets(self) -> list[Asset]:
        """List all assets.

        Returns:
            list[Asset]: All asset entries within the database.
        """

        LOGGER.debug("Listing assets")

        cursor = self._connection.cursor()

        cursor.execute("SELECT * FROM assets ORDER BY name ASC, type ASC")

        assets = []
        for row in cursor.fetchall():
            assets.append(
                Asset(
                    id=row["asset_id"],
                    name=row["name"],
                    asset_type=AssetType(row["type"]),
                )
            )

        return assets

    def list_asset_versions(self, asset_id: int) -> list[AssetVersion]:
        """List all asset versions for a specific asset.

        Args:
            asset_id (int): The id necessary to retrieve all associated versions.

        Returns:
            list[AssetVersion]: All asset versions corresponding to an asset with the
                provided id.
        """

        LOGGER.debug("Listing asset versions for {}".format(asset_id))

        cursor = self._connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM asset_versions
            WHERE asset_id = ?
            ORDER BY department, version, status
            """,
            (asset_id,),
        )

        asset_versions = []
        for row in cursor.fetchall():
            asset_versions.append(
                AssetVersion(
                    asset=asset_id,
                    department=row["department"],
                    version=row["version"],
                    status=VersionStatus(row["status"]),
                )
            )

        return asset_versions

    def close(self) -> None:
        """Safely close the connection."""

        self._connection.close()
