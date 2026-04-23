from __future__ import annotations

from enum import Enum

import numpy as np

from units import Angle, AngleUnit


class OutputFovBasis(Enum):
    """
    Basis used to interpret output_fov.

    VERTICAL means output_fov is treated as vertical FoV.
    HORIZONTAL means output_fov is treated as horizontal FoV.
    """

    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"

    def build_output_fovs(
        self,
        output_fov: Angle,
        aspect_ratio: float,
    ) -> tuple[Angle, Angle]:
        base_fov_radian = np.asarray(output_fov.radian, dtype=np.float64)
        half_tangent = np.tan(base_fov_radian / 2.0)

        match self:
            case OutputFovBasis.VERTICAL:
                output_vfov_radian = base_fov_radian
                output_hfov_radian = 2.0 * np.arctan(half_tangent * aspect_ratio)
            case OutputFovBasis.HORIZONTAL:
                output_hfov_radian = base_fov_radian
                output_vfov_radian = 2.0 * np.arctan(half_tangent / aspect_ratio)

        degree = AngleUnit.DEGREE
        output_hfov = Angle(value=np.rad2deg(output_hfov_radian), unit=degree)
        output_vfov = Angle(value=np.rad2deg(output_vfov_radian), unit=degree)
        return output_hfov, output_vfov
