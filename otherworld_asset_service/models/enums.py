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


class Department(Enum):
    """Represents all valid departments."""

    ANIMATION = "animation"
    CFX = "cfx"
    FX = "fx"
    MODELING = "modeling"
    RIGGING = "rigging"
    TEXTURING = "texturing"


class Status(Enum):
    """Represents all valid asset version statuses."""

    ACTIVE = "active"
    INACTIVE = "inactive"
