from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class SphericalCoordinates:
    longitude: np.ndarray
    latitude: np.ndarray

    @property
    def u_coordinates(self) -> np.ndarray:
        return np.mod((self.longitude / (2 * np.pi)) + 0.5, 1.0)

    @property
    def v_coordinates(self) -> np.ndarray:
        return np.clip(0.5 - (self.latitude / np.pi), 0.0, 1.0)

    @classmethod
    def hypotenuse(
        cls,
        x_coordinates: np.ndarray,
        y_coordinates: np.ndarray,
    ) -> np.ndarray:
        return np.sqrt(x_coordinates**2 + y_coordinates**2)

    @classmethod
    def from_cartesian(
        cls,
        x_coordinates: np.ndarray,
        y_coordinates: np.ndarray,
        z_coordinates: np.ndarray,
    ) -> SphericalCoordinates:
        longitude = np.arctan2(y_coordinates, x_coordinates)
        latitude = np.arctan2(
            z_coordinates,
            cls.hypotenuse(x_coordinates=x_coordinates, y_coordinates=y_coordinates),
        )
        return cls(longitude=longitude, latitude=latitude)
