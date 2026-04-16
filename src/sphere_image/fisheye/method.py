from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from .processor import FisheyeProcessor

class FisheyeProjectionMethod(Enum):
    """
    Method of fisheye projection.
    """
    ORTHOGRAPHIC = "Orthographic"
    EQUIDISTANT = "Equidistant"
    STEREOGRAPHIC = "Stereographic"
    EQUAL_SOLID_ANGLE = "EqualSolidAngle"

    @property
    def processor_class(self) -> Type[FisheyeProcessor]:
        match self:
            case FisheyeProjectionMethod.EQUIDISTANT:
                from .processors import EquidistantFisheyeProcessor
                return EquidistantFisheyeProcessor
            case _:
                raise ValueError(f"Not implemented error. -> method: {self}")


    