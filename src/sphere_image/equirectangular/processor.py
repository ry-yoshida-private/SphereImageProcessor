from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import cv2
import numpy as np

from rotation import RotationMatrix

from .parameter import EquirectangularProcessorParameters


@dataclass
class EquirectangularProcessor(ABC):
    image: np.ndarray
    params: EquirectangularProcessorParameters = field(
        default_factory=EquirectangularProcessorParameters
    )

    @abstractmethod
    def _map_rotation_to_uv(
        self,
        rotation_matrix: RotationMatrix,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Return normalized source image coordinates (u, v) for remap.
        
        Parameters
        ----------
        rotation_matrix: RotationMatrix
            Rotation matrix.

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            The u and v coordinates.
        """

    def run_pipeline(self, rotation_matrix: RotationMatrix) -> np.ndarray:
        """
        Run the equirectangular remapping pipeline.

        
        """
        u_coordinates, v_coordinates = self._map_rotation_to_uv(
            rotation_matrix=rotation_matrix
        )
        return self.remap(
            u_coordinates=u_coordinates,
            v_coordinates=v_coordinates,
        )

    def _create_direction_vector_grid(self) -> np.ndarray:
        """
        Generate normalized 3D direction vectors for each output pixel.
        """
        horizontal_coordinates = np.linspace(
            -np.tan(self.params.output_hfov.radian / 2),
            np.tan(self.params.output_hfov.radian / 2),
            self.params.output_image_w,
        )
        vertical_coordinates = np.linspace(
            -np.tan(self.params.output_vfov.radian / 2),
            np.tan(self.params.output_vfov.radian / 2),
            self.params.output_image_h,
        )

        if self.params.is_camera_pointing_up:
            vertical_coordinates *= -1

        horizontal_grid, vertical_grid = np.meshgrid(
            horizontal_coordinates,
            vertical_coordinates,
        )
        depth_grid = np.ones_like(horizontal_grid)
        direction_vectors = np.stack(
            [depth_grid, horizontal_grid, vertical_grid],
            axis=-1,
        )
        direction_vectors /= np.linalg.norm(direction_vectors, axis=-1, keepdims=True)
        return direction_vectors.reshape(-1, 3)

    def remap(
        self,
        u_coordinates: np.ndarray,
        v_coordinates: np.ndarray,
    ) -> np.ndarray:
        """
        Remap the image using normalized source coordinates.
        """
        x_pixel_coordinate = (u_coordinates * self.image.shape[1]).astype(np.float32)
        y_pixel_coordinate = (v_coordinates * self.image.shape[0]).astype(np.float32)
        return cv2.remap(
            self.image,
            x_pixel_coordinate,
            y_pixel_coordinate,
            interpolation=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_WRAP,
        )

    @classmethod
    def from_path(
        cls,
        path: str,
        params: EquirectangularProcessorParameters | None = None,
    ) -> EquirectangularProcessor:
        image = cv2.imread(path)
        if image is None:
            raise ValueError(f"Failed to read image: {path}")

        selected_params = params or EquirectangularProcessorParameters()
        if cls is EquirectangularProcessor:
            return selected_params.build_processor(image=image)
        return cls(image=image, params=selected_params)