from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from .processor import EquirectangularProcessor


class EquirectangularProjectionMethod(Enum):
    """
    Method for remapping from equirectangular image.
    """

    PERSPECTIVE = "Perspective"
    ORTHOGRAPHIC = "Orthographic"
    STEREOGRAPHIC = "Stereographic"
    EQUIDISTANT = "Equidistant"
    EQUAL_AREA = "EqualArea"
    CYLINDRICAL = "Cylindrical"
    MERCATOR = "Mercator"
    LAMBERT_CYLINDRICAL = "LambertCylindrical"

    @property
    def processor_class(self) -> Type[EquirectangularProcessor]:
        match self:
            case EquirectangularProjectionMethod.PERSPECTIVE:
                from .processors import PerspectiveEquirectangularProcessor

                return PerspectiveEquirectangularProcessor
            case _:
                raise ValueError(f"Not implemented error. -> method: {self}")
