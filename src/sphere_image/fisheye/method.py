from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from .processor import FisheyeProcessor

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

    @property
    def processor_class(self) -> Type[FisheyeProcessor]:
        """
        Return the processor class for the fisheye projection method.
        
        Returns:
        --------
        Type[FisheyeProcessor]
            The processor class for the fisheye projection method.
        """
        match self:
            case FisheyeProjectionMethod.ORTHOGRAPHIC:
                from .processors import OrthographicFisheyeProcessor
                return OrthographicFisheyeProcessor
            case FisheyeProjectionMethod.EQUIDISTANT:
                from .processors import EquidistantFisheyeProcessor
                return EquidistantFisheyeProcessor
            case FisheyeProjectionMethod.STEREOGRAPHIC:
                from .processors import StereographicFisheyeProcessor
                return StereographicFisheyeProcessor
            case FisheyeProjectionMethod.EQUISOLID:
                from .processors import EquisolidFisheyeProcessor
                return EquisolidFisheyeProcessor

