from __future__ import annotations

import argparse

import cv2
import numpy as np

from rotation import RotationMatrix

from ..parameter import EquirectangularProcessorParameters
from ..processor import EquirectangularProcessor


class PerspectiveEquirectangularProcessor(EquirectangularProcessor):
    """
    Equirectangular -> perspective remapping processor.
    """

    def _map_rotation_to_uv(
        self,
        rotation_matrix: RotationMatrix,
    ) -> tuple[np.ndarray, np.ndarray]:
        direction_vectors = self._create_direction_vector_grid()
        rotated_direction_vectors = direction_vectors @ rotation_matrix.T

        x_coordinates = rotated_direction_vectors[:, 0]
        y_coordinates = rotated_direction_vectors[:, 1]
        z_coordinates = rotated_direction_vectors[:, 2]

        longitude = np.arctan2(y_coordinates, x_coordinates)
        hypotenuse = np.sqrt(x_coordinates**2 + y_coordinates**2)
        latitude = np.arctan2(z_coordinates, hypotenuse)

        u_coordinates = (longitude / (2 * np.pi)) + 0.5
        v_coordinates = 0.5 - (latitude / np.pi)
        u_coordinates = np.mod(u_coordinates, 1.0)
        v_coordinates = np.clip(v_coordinates, 0.0, 1.0)

        return (
            u_coordinates.reshape(self.params.output_image_h, self.params.output_image_w),
            v_coordinates.reshape(self.params.output_image_h, self.params.output_image_w),
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remap an equirectangular image to a perspective view."
    )
    parser.add_argument(
        "-i",
        "--input",
        default="image/equirectangular.JPG",
        help="Path to the input equirectangular image.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="tmp_equirectangular.jpg",
        help="Path to write the output image.",
    )
    parser.add_argument(
        "--camera-pointing-up",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Override camera vertical orientation (default: EquirectangularProcessorParameters).",
    )
    args = parser.parse_args()

    image = cv2.imread(args.input)
    if image is None:
        raise ValueError(f"Failed to read image: {args.input}")

    if args.camera_pointing_up is not None:
        params = EquirectangularProcessorParameters(
            is_camera_pointing_up=args.camera_pointing_up
        )
    else:
        params = EquirectangularProcessorParameters()

    processor = PerspectiveEquirectangularProcessor(image=image, params=params)
    rotation_matrix = RotationMatrix.unit_matrix()
    output_image = processor.run_pipeline(rotation_matrix=rotation_matrix)
    if not cv2.imwrite(args.output, output_image):
        raise RuntimeError(f"Failed to write image: {args.output}")


if __name__ == "__main__":
    main()
