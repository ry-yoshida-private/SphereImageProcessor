from __future__ import annotations

import argparse
from typing import Type

from ..processor import FisheyeProcessor
from .equidistant import EquidistantFisheyeProcessor
from .equisolid import EquisolidFisheyeProcessor
from .orthographic import OrthographicFisheyeProcessor
from .stereographic import StereographicFisheyeProcessor
from .utils import (
    build_processor_params,
    compose_rotation_matrix_from_euler,
    read_required_image,
    write_required_image,
)

PROCESSOR_MAP: dict[str, Type[FisheyeProcessor]] = {
    "equidistant": EquidistantFisheyeProcessor,
    "orthographic": OrthographicFisheyeProcessor,
    "stereographic": StereographicFisheyeProcessor,
    "equisolid": EquisolidFisheyeProcessor,
}


def build_processors_cli_parser() -> argparse.ArgumentParser:
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
        choices=tuple(PROCESSOR_MAP.keys()),
        default="equidistant",
        help="Single projection method to run.",
    )
    return parser


def main() -> None:
    parser = build_processors_cli_parser()
    args = parser.parse_args()
    image = read_required_image(args.input)
    params = build_processor_params(args.camera_pointing_up)
    rotation_matrix = compose_rotation_matrix_from_euler(
        yaw_deg=args.yaw_deg,
        pitch_deg=args.pitch_deg,
        roll_deg=args.roll_deg,
    )

    processor = PROCESSOR_MAP[args.method](image=image, params=params)
    output_image = processor.run_pipeline(rotation_matrix=rotation_matrix)
    write_required_image(args.output, output_image)
    print(f"saved {args.method}: {args.output}")


if __name__ == "__main__":
    main()
