from dataclasses import dataclass

from otherworld_asset_service.models.enums import Department, VersionStatus


@dataclass(slots=True)
class Version:
    """An iteration for a specific asset state

    Version uniqueness is defined by its referenced asset, department, and version
    number. Only a single version can be created with this specific combination.
    Versions increment linearly by integer values.
    """

    asset_id: int
    department: Department
    number: int = 1
    status: VersionStatus = VersionStatus.INACTIVE

    def __post_init__(self):
        if self.number < 1:
            raise ValueError("Version number must be greater than or equal to 1")
