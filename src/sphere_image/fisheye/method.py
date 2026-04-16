from __future__ import annotations

from enum import Enum
import numpy as np
from units import Angle

class FisheyeProjectionMethod(Enum):
    """
    Method of fisheye projection.
    
    Attributes
    ----------
    ORTHOGRAPHIC: FisheyeProjectionMethod
        Orthographic projection method.
    EQUIDISTANT: FisheyeProjectionMethod
        Equidistant projection method.
    STEREOGRAPHIC: FisheyeProjectionMethod
        Stereographic projection method.
    EQUISOLID: FisheyeProjectionMethod
        Equisolid projection method.
    """
    ORTHOGRAPHIC = "Orthographic"
    EQUIDISTANT = "Equidistant"
    STEREOGRAPHIC = "Stereographic"
    EQUISOLID = "Equisolid"

    def calculate_radius(self, f: float, angle: Angle) -> np.ndarray:
        match self:
            case FisheyeProjectionMethod.EQUIDISTANT:
                return angle.value / f
            case FisheyeProjectionMethod.ORTHOGRAPHIC:
                return np.sin(angle.value) / np.sin(f)
            case FisheyeProjectionMethod.STEREOGRAPHIC:
                return np.tan(angle.value / 2) / np.tan(f / 2)
            case FisheyeProjectionMethod.EQUISOLID:
                return np.sin(angle.value / 2) / np.sin(f / 2)
