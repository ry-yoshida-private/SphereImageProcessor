from __future__ import annotations

from enum import Enum


class EquirectangularProjectionMethod(Enum):
    """
    Method for remapping from equirectangular image.

    Attributes
    ----------
    PERSPECTIVE: EquirectangularProjectionMethod
        Perspective projection.
    ORTHOGRAPHIC: EquirectangularProjectionMethod
        Orthographic projection.
    STEREOGRAPHIC: EquirectangularProjectionMethod
        Stereographic projection.
    EQUIDISTANT: EquirectangularProjectionMethod
        Equidistant projection.
    EQUAL_AREA: EquirectangularProjectionMethod
        Equal-area projection.
    CYLINDRICAL: EquirectangularProjectionMethod
        Cylindrical projection.
    MERCATOR: EquirectangularProjectionMethod
        Mercator projection.
    LAMBERT_CYLINDRICAL: EquirectangularProjectionMethod
        Lambert cylindrical projection.
    """

    PERSPECTIVE = "Perspective"
    ORTHOGRAPHIC = "Orthographic"
    STEREOGRAPHIC = "Stereographic"
    EQUIDISTANT = "Equidistant"
    EQUAL_AREA = "EqualArea"
    CYLINDRICAL = "Cylindrical"
    MERCATOR = "Mercator"
    LAMBERT_CYLINDRICAL = "LambertCylindrical"
