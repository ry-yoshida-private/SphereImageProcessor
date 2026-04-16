import numpy as np

from ..processor import FisheyeProcessor

from rotation import RotationMatrix
from geometry.planar import PolarCoordinate
from geometry.spatial import Vectors3D
from units import Angle


class EquisolidFisheyeProcessor(FisheyeProcessor):
    """
    Fisheye remapping using equisolid-angle projection model.
    """

    def _map_rotation_to_uv(
        self,
        rotation_matrix: RotationMatrix,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Convert fisheye image to equisolid-angle image.

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
        max_incident_angle = self.params.camera_hfov.radian / 2
        radius: np.ndarray = np.sin(azimuthal_angles.value / 2) / np.sin(
            max_incident_angle / 2
        )
        polar_coordinate = PolarCoordinate(
            radius=radius,
            angle=polar_angles,
        )
        return self._PolarCoordinate2NormalizedCartesianCoordinate(
            polar_coordinate=polar_coordinate
        )
