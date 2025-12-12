from enum import Enum


class AssetType(Enum):
    """Represents all valid asset types."""

    CHARACTER = "character"
    DRESSING = "dressing"
    ENVIRONMENT = "environment"
    FX = "fx"
    PROP = "prop"
    SET = "set"
    VEHICLE = "vehicle"


class VersionStatus(Enum):
    """Represents all valid asset version statuses."""

    ACTIVE = "active"
    INACTIVE = "inactive"
