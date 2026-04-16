from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from functools import cached_property
from typing import TYPE_CHECKING

from .method import FisheyeProjectionMethod

if TYPE_CHECKING:
    from .processor import FisheyeProcessor
from units import Angle, AngleUnit

@dataclass
class FisheyeProcessorParameters:
    """
    Parameters for fisheye processor(class for transforming fisheye image to equidistant image).
    
    Attributes
    ----------
    camera_hfov: Angle
        The horizontal field of view of the camera.
    camera_vfov: Angle
        The vertical field of view of the camera.
    output_hfov: Angle
        The horizontal field of view of the output image.
    method: FisheyeProjectionMethod
        The method to use for transforming the fisheye image to equidistant image.
    output_image_w: int
        The width of the output image.
    output_image_h: int
        The height of the output image.
    is_camera_pointing_up: bool
        Whether the camera is pointing up or down(True: up, False: down).
    """
    camera_hfov: Angle = field(default_factory=lambda: Angle(value=np.array([185]), unit=AngleUnit.DEGREE))
    camera_vfov: Angle = field(default_factory=lambda: Angle(value=np.array([185]), unit=AngleUnit.DEGREE))
    output_hfov: Angle = field(default_factory=lambda: Angle(value=np.array([90]), unit=AngleUnit.DEGREE))
    method: FisheyeProjectionMethod = field(default_factory=lambda: FisheyeProjectionMethod.EQUIDISTANT)

    output_image_w: int = 1280
    output_image_h: int = 720
    is_camera_pointing_up: bool = True

    def __post_init__(self) -> None:
        for field_name, angle in (
            ("camera_hfov", self.camera_hfov),
            ("camera_vfov", self.camera_vfov),
            ("output_hfov", self.output_hfov),
        ):
            value = np.asarray(angle.value)
            if value.size != 1:
                raise ValueError(
                    f"{field_name} must contain exactly one element, got {value.size}."
                )

    @property
    def aspect_ratio(self) -> float:
        return self.output_image_w / self.output_image_h
    
    @cached_property
    def output_vfov(self) -> Angle:
        return Angle(
            value=self.output_hfov.degree / self.aspect_ratio,
            unit=AngleUnit.DEGREE,
        )

    def build_processor(self, image: np.ndarray) -> FisheyeProcessor:
        """
        Build a fisheye processor configured with this parameter set.

        Parameters
        ----------
        image: np.ndarray
            The image to process.

        Returns
        -------
        FisheyeProcessor
            Processor instance that applies self.method in radius mapping.
        """
        from .processor import FisheyeProcessor

        return FisheyeProcessor(image=image, params=self)