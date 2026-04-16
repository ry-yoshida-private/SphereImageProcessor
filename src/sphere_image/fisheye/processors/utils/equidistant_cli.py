from __future__ import annotations

import argparse

import cv2
import numpy as np

from ...parameter import FisheyeProcessorParameters
from rotation import RotationMatrix


def compose_rotation_matrix_from_euler(
    yaw_deg: float,
    pitch_deg: float,
    roll_deg: float,
) -> RotationMatrix:
    """
    Build camera rotation matrix from Euler angles.

    Axis convention:
    - forward: +X
    - right:   +Y
    - up:      +Z

    Angle convention:
    - yaw   (+): look to the right (around +Z)
    - pitch (+): look upward (around +Y)
    - roll  (+): clockwise in image plane (around +X)
    """
    yaw = np.deg2rad(yaw_deg)
    # Use negative sign so positive pitch means "look upward".
    pitch = -np.deg2rad(pitch_deg)
    roll = -np.deg2rad(roll_deg)

    rotation_z = np.array(
        [
            [np.cos(yaw), -np.sin(yaw), 0.0],
            [np.sin(yaw), np.cos(yaw), 0.0],
            [0.0, 0.0, 1.0],
        ],
        dtype=np.float64,
    )
    rotation_y = np.array(
        [
            [np.cos(pitch), 0.0, np.sin(pitch)],
            [0.0, 1.0, 0.0],
            [-np.sin(pitch), 0.0, np.cos(pitch)],
        ],
        dtype=np.float64,
    )
    rotation_x = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, np.cos(roll), -np.sin(roll)],
            [0.0, np.sin(roll), np.cos(roll)],
        ],
        dtype=np.float64,
    )
    return RotationMatrix(rotation_z @ rotation_y @ rotation_x)


def build_equidistant_cli_parser() -> argparse.ArgumentParser:
    """
    Build CLI parser for equidistant fisheye remapping.
    """
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
    parser.add_argument(
        "--yaw-deg",
        type=float,
        default=0.0,
        help="Yaw angle in degrees (+: look right).",
    )
    parser.add_argument(
        "--pitch-deg",
        type=float,
        default=0.0,
        help="Pitch angle in degrees (+: look up).",
    )
    parser.add_argument(
        "--roll-deg",
        type=float,
        default=0.0,
        help="Roll angle in degrees (+: clockwise image tilt).",
    )
    return parser


def build_processor_params(camera_pointing_up: bool | None) -> FisheyeProcessorParameters:
    """
    Build processor parameters from optional CLI override.
    """
    if camera_pointing_up is not None:
        return FisheyeProcessorParameters(is_camera_pointing_up=camera_pointing_up)
    return FisheyeProcessorParameters()


def read_required_image(image_path: str) -> np.ndarray:
    """
    Read image file and raise when not found.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to read image: {image_path}")
    return image


def write_required_image(image_path: str, image: np.ndarray) -> None:
    """
    Write image file and raise when write fails.
    """
    if not cv2.imwrite(image_path, image):
        raise RuntimeError(f"Failed to write image: {image_path}")
