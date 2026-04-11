import argparse

import cv2
import numpy as np

from ..parameter import FisheyeProcessorParameters
from ..processor import FisheyeProcessor

from rotation import RotationMatrix
from geometry.planar import PolarCoordinate
from geometry.spatial import Vectors3D
from units import Angle


class EquidistantFisheyeProcessor(FisheyeProcessor):
    """
    Fisheye → rectilinear-style mapping using equidistant projection model.
    
    Attributes
    ---------- 
    image: np.ndarray
        The image to process.
    params: FisheyeProcessorParameters
        Parameters for fisheye processor.
    """

    def _map_rotation_to_uv(
        self,
        rotation_matrix: RotationMatrix,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Convert fisheye image to equidistant image.

        ** Tips **
        u: horizontal axis of image(screen) coordinate system
           u=r*cosθ
        v: vertical axis of image(screen) coordinate system

        Parameters
        ----------
        rotation_matrix: RotationMatrix
            Rotation matrix.

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            The u and v coordinates.
        """
        direction_vectors: Vectors3D = self._create_direction_vector_grid()
        rotated_direction_vectors: Vectors3D = Vectors3D(
            value=direction_vectors.value @ rotation_matrix.T
        )
        azimuthal_angles: Angle = rotated_direction_vectors.to_azimuthal_angles(
            up_index=2
        )
        polar_angles: Angle = rotated_direction_vectors.to_polar_angles(
            forward_index=0,
            right_index=1,
        )
        radius: np.ndarray = azimuthal_angles.value / (
            self.params.camera_hfov.radian / 2
        )
        polar_coordinate = PolarCoordinate(
            radius=radius,
            angle=polar_angles,
        )
        u_coordinates, v_coordinates = (
            self._PolarCoordinate2NormalizedCartesianCoordinate(
                polar_coordinate=polar_coordinate
            )
        )
        return u_coordinates, v_coordinates


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remap a fisheye image to an equidistant (rectilinear-style) view.",
    )
    parser.add_argument(
        "-i",
        "--input",
        default="data/input_fisheye.jpg",
        help="Path to the input fisheye image.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="tmp_fisheye.jpg",
        help="Path to write the output image.",
    )
    parser.add_argument(
        "--camera-pointing-up",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Override camera vertical orientation (default: FisheyeProcessorParameters).",
    )
    args = parser.parse_args()

    image = cv2.imread(args.input)
    if image is None:
        raise ValueError(f"Failed to read image: {args.input}")

    print(f"image.shape: {image.shape}")

    if args.camera_pointing_up is not None:
        params = FisheyeProcessorParameters(
            is_camera_pointing_up=args.camera_pointing_up
        )
    else:
        params = FisheyeProcessorParameters()

    processor = EquidistantFisheyeProcessor(image=image, params=params)
    rotation_matrix = RotationMatrix.unit_matrix()
    output_image = processor.run_pipeline(rotation_matrix=rotation_matrix)
    if not cv2.imwrite(args.output, output_image):
        raise RuntimeError(f"Failed to write image: {args.output}")


if __name__ == "__main__":
    main()
