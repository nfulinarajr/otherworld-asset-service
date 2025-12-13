import argparse
import re

from pathlib import Path

from otherworld_asset_service.api.validation.pipelines.asset_pipeline import (
    build_default_asset_pipeline,
)
from otherworld_asset_service.api.validation.pipelines.asset_version_pipeline import (
    build_default_asset_version_pipeline,
)
from otherworld_asset_service.api.service import OtherWorldAssetService
from otherworld_asset_service.storage.sqlite_database import SQLiteDatabase
from otherworld_asset_service.models.asset import Asset
from otherworld_asset_service.models.asset_version import AssetVersion
from otherworld_asset_service.models.enums import AssetType, VersionStatus


def get_asset_type_from_input() -> AssetType | None:
    """Get the asset type from the user input

    Returns:
        AssetType | None: The asset type from valid user input, or None if not.
    """

    print_asset_types()

    user_input = input("\nPlease provide a type for your asset: ").strip().lower()

    try:
        if user_input.startswith(("1", "1.")):
            asset_type = AssetType("character")
        elif user_input.startswith(("2", "2.")):
            asset_type = AssetType("dressing")
        elif user_input.startswith(("3", "3.")):
            asset_type = AssetType("environment")
        elif user_input.startswith(("4", "4.")):
            asset_type = AssetType("fx")
        elif user_input.startswith(("5", "5.")):
            asset_type = AssetType("prop")
        elif user_input.startswith(("6", "6.")):
            asset_type = AssetType("set")
        elif user_input.startswith(("7", "7.")):
            asset_type = AssetType("vehicle")
        else:
            asset_type = AssetType(user_input)
    except ValueError as error:
        print("\n{} is not a valid asset type: {}".format(error))
        asset_type = None

    return asset_type


def get_version_status_from_input() -> VersionStatus | None:
    """Get the version status from the user input.

    Returns:
        VersionStatus | None: The version status from valid user input, or None if not.
    """

    print_version_statuses()

    user_input = input("\nPlease provide a version status: ").strip().lower()

    try:
        if user_input.startswith(("1", "1.")):
            version_status = VersionStatus("active")
        elif user_input.startswith(("2", "2.")):
            version_status = VersionStatus("inactive")
        else:
            version_status = VersionStatus(user_input)
    except ValueError:
        print("\n{} is not a valid version status.".format(user_input))
        version_status = None

    return version_status


def print_asset_types():
    print("\n***********")
    print("Asset Types")
    print("***********")
    print("\n1. character")
    print("2. dressing")
    print("3. environment")
    print("4. fx")
    print("5. prop")
    print("6. set")
    print("7. vehicle")


def print_asset_version_info(asset: Asset, asset_version: AssetVersion):
    print("\nAsset Name: {} ({})".format(asset.name, asset.asset_type.value))
    print("\nDepartment: {}".format(asset_version.department))
    print("Version Number: {}".format(asset_version.version))
    print("Status: {}".format(asset_version.status.value))


def print_main_menu():
    print("\n*************************")
    print("Other World Asset Service")
    print("*************************")
    print(
        "\nWelcome to the Other World Asset Service!\n\nThis is a simple Asset and "
        "Asset Version API for...THE OTHER WORLD!!! (dun, dun dun)\n\nWhat would you "
        "like to do?"
    )
    print("\n1. Load assets")
    print("2. Add asset")
    print("3. Add asset version")
    print("4. Get asset")
    print("5. Get asset version")
    print("6. List assets")
    print("7. List asset versions")
    print("8. Exit")


def print_version_statuses():
    print("\n****************")
    print("Version Statuses")
    print("****************")
    print("1. active")
    print("2. inactive")


def build_parser() -> argparse.ArgumentParser:
    """Parse arguments.

    Returns:
        argparse.ArgumentParser: The ArgumentParser object
    """

    parser = argparse.ArgumentParser(
        prog="Other World Asset Service CLI",
        description="A simple asset and asset version management API",
    )

    parser.add_argument(
        "--data-store-path",
        type=Path,
        default=None,
        help="The path to your data_store file (default: None)",
    )

    return parser


def create_asset_service(data_store: Path | None) -> OtherWorldAssetService:
    """Create the asset service to interact with the data store.

    Args:
        data_store (Path): The data store location.

    Returns:
        OtherWorldAssetService: The asset service.
    """

    if not data_store:
        data_store = SQLiteDatabase()

    asset_pipeline = build_default_asset_pipeline()
    asset_version_pipeline = build_default_asset_version_pipeline()

    asset_service = OtherWorldAssetService(
        data_store, asset_pipeline, asset_version_pipeline
    )
    return asset_service


def launch_menu_loop(asset_service: OtherWorldAssetService):
    """The main CLI menu loop.

    Args:
        asset_service (OtherWorldAssetService): The asset service to execute actions on.
    """

    while True:
        print_main_menu()

        choice = input("> ").strip().lower()

        if choice == "1":
            user_input = input("\nPlease provide a JSON file path to load: ").strip()

            # Handle empty submission
            if not user_input:
                print("\nNo file path was provided.")
                continue

            file_path = Path(user_input)

            # Check file path validity
            if not file_path.is_file() or not user_input.endswith(".json"):
                print("\n{} is not a valid JSON file.".format(file_path))
                continue

            try:
                asset_service.load_assets(file_path)
            except Exception as error:
                print("Error loading assets: {}".format(error))
        elif choice == "2":
            asset_name = (
                input("\nPlease provide a name for your asset: ").strip().lower()
            )

            asset_type = get_asset_type_from_input()

            if asset_type is None:
                print("Could not add {} due to invalid input.".format(asset_name))

            try:
                asset_service.add_asset(Asset(asset_name, asset_type))
            except Exception as error:
                print("\nError adding the asset: {}".format(error))
        elif choice == "3":
            asset_name = input("\nPlease provide the asset name: ").strip().lower()

            asset_type = get_asset_type_from_input()
            department = input("Please provide a department: ").strip().lower()
            version = input("Please provide a version: ").strip().lower()
            version_status = get_version_status_from_input()

            # Determine if an asset exists with the same name and create one if not
            asset = asset_service.get_asset(asset_name)

            if not asset:
                try:
                    asset = asset_service.add_asset(Asset(asset_name, asset_type))
                except Exception as error:
                    print("Error adding the asset: {}".format(error))
                    continue

            try:
                asset_version = AssetVersion(
                    asset.id, department, int(version), version_status
                )
                asset_service.add_asset_version(asset, asset_version)
            except Exception as error:
                print("Error adding the asset version: {}".format(error))
        elif choice == "4":
            asset_name = input("\nPlease provide the asset name: ").strip().lower()

            try:
                asset = asset_service.get_asset(asset_name)

                if asset:
                    print(
                        "\nAsset Name: {} ({})".format(
                            asset.name, asset.asset_type.value
                        )
                    )
                else:
                    print("\nCould not find an asset for {}".format(asset_name))
            except Exception as error:
                print("Error getting asset: ".format(error))
        elif choice == "5":
            asset_name = input("\nPlease provide the asset name: ").strip().lower()

            asset = asset_service.get_asset(asset_name)

            if not asset:
                print("\nCould not find an asset for {}".format(asset_name))
                continue

            version = input("Please provide the version number: ").strip().lower()

            try:
                asset_version = asset_service.get_asset_version(asset_name, version)

                if asset_version:
                    print_asset_version_info(asset, asset_version)
                else:
                    print(
                        "\nCould not find version {} for {}".format(version, asset_name)
                    )
            except Exception as error:
                print("\nError getting asset version: {}".format(error))
        elif choice == "6":
            for asset in asset_service.list_assets():
                print(
                    "\nAsset Name: {} ({})".format(asset.name, asset.asset_type.value)
                )
        elif choice == "7":
            asset_name = input("\nPlease provide the asset name: ").strip().lower()

            asset = asset_service.get_asset(asset_name)

            if not asset:
                print("\nCould not find an asset for {}".format(asset_name))
                continue

            print("\nAsset Name: {} ({})".format(asset.name, asset.asset_type.value))

            for asset_version in asset_service.list_asset_versions(asset_name):
                print("\nDepartment: {}".format(asset_version.department))
                print("Version Number: {}".format(asset_version.version))
                print("Status: {}".format(asset_version.status.value))
        elif choice == "8":
            break
        else:
            print("\nInvalid option. Please try again.")


def launch_asset_service_cli(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    asset_service = create_asset_service(args.data_store_path)

    launch_menu_loop(asset_service)
