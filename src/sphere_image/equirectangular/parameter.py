from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from typing import TYPE_CHECKING

import numpy as np

from units import Angle, AngleUnit

from .method import EquirectangularProjectionMethod

if TYPE_CHECKING:
    from .processor import EquirectangularProcessor


@dataclass
class EquirectangularProcessorParameters:
    """
    Parameters for equirectangular processor.
    """

    output_hfov: Angle = field(
        default_factory=lambda: Angle(value=np.array([90]), unit=AngleUnit.DEGREE)
    )
    method: EquirectangularProjectionMethod = field(
        default_factory=lambda: EquirectangularProjectionMethod.PERSPECTIVE
    )
    output_image_w: int = 1280
    output_image_h: int = 720
    is_camera_pointing_up: bool = True

    @property
    def aspect_ratio(self) -> float:
        return self.output_image_w / self.output_image_h

    @cached_property
    def output_vfov(self) -> Angle:
        return Angle(
            value=self.output_hfov.degree / self.aspect_ratio,
            unit=AngleUnit.DEGREE,
        )

    def build_processor(self, image: np.ndarray) -> EquirectangularProcessor:
        """
        Return a concrete EquirectangularProcessor for self.method.
        """
        return self.method.processor_class(image=image, params=self)
