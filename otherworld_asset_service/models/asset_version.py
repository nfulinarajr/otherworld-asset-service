from dataclasses import dataclass

from otherworld_asset_service.models.enums import VersionStatus


@dataclass(slots=True)
class AssetVersion:
    """A single iteration describing a specific asset state.

    Asset version uniqueness is defined by its asset, department, and version. Only a
    single asset version can be created with this specific combination. Asset versions
    increment linearly by integer values.
    """

    asset: int
    department: str
    version: int = 1
    status: VersionStatus = VersionStatus.INACTIVE

    def __post_init__(self):
        if self.version < 1:
            raise ValueError("Asset version must be greater than or equal to 1")
