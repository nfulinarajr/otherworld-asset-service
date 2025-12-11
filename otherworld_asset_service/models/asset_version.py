from dataclasses import dataclass

from otherworld_asset_service.models.enums import Department, Status


@dataclass(slots=True)
class AssetVersion:
    """A single iteration for a specific asset state

    Asset version uniqueness is defined by its asset, department, and version. Only a
    single asset version can be created with this specific combination. Asset versions
    increment linearly by integer values.
    """

    asset: int
    department: Department
    version: int = 1
    status: Status = Status.INACTIVE

    def __post_init__(self):
        if self.version < 1:
            raise ValueError("Asset version must be greater than or equal to 1")
