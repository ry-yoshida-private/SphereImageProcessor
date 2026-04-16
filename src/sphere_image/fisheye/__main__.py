from __future__ import annotations

import argparse

import cv2
import numpy as np

from .method import FisheyeProjectionMethod
from .parameter import FisheyeProcessorParameters
from rotation import RotationMatrix


def compose_rotation_matrix_from_euler(
    yaw_deg: float,
    pitch_deg: float,
    roll_deg: float,
) -> RotationMatrix:
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


def read_required_image(image_path: str) -> np.ndarray:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to read image: {image_path}")
    return image


def write_required_image(image_path: str, image: np.ndarray) -> None:
    if not cv2.imwrite(image_path, image):
        raise RuntimeError(f"Failed to write image: {image_path}")


def build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Remap a fisheye image with a projection method.",
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
    parser.add_argument(
        "--method",
        choices=tuple(method.name.lower() for method in FisheyeProjectionMethod),
        default=FisheyeProjectionMethod.EQUIDISTANT.name.lower(),
        help="Single projection method to run.",
    )
    return parser


def main() -> None:
    parser = build_cli_parser()
    args = parser.parse_args()
    image = read_required_image(args.input)

    method = FisheyeProjectionMethod[args.method.upper()]
    params = FisheyeProcessorParameters(method=method)
    if args.camera_pointing_up is not None:
        params.is_camera_pointing_up = args.camera_pointing_up

    rotation_matrix = compose_rotation_matrix_from_euler(
        yaw_deg=args.yaw_deg,
        pitch_deg=args.pitch_deg,
        roll_deg=args.roll_deg,
    )
    processor = params.build_processor(image=image)
    output_image = processor.run_pipeline(rotation_matrix=rotation_matrix)
    write_required_image(args.output, output_image)
    print(f"saved {args.method}: {args.output}")


if __name__ == "__main__":
    main()
