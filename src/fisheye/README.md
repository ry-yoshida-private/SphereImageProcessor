# fisheye

## Overview

This package maps fisheye input to a pinhole-like image by sampling the fisheye texture along rays derived from output FOV and an optional world rotation. Shared logic lives on the abstract `FisheyeProcessor`; concrete models live under `processors/`.

Equidistant projection is implemented today; other `FisheyeProjectionMethod` values are reserved for future work. Details for the equidistant path and CLI: [processors/README.md](./processors/README.md).

## Components

| Component | Description |
| --- | --- |
| [parameter.py](./parameter.py) | `FisheyeProcessorParameters` (FOV, resolution, method, vertical flip) and `build_processor()`. |
| [method.py](./method.py) | `FisheyeProjectionMethod` enum. |
| [processor.py](./processor.py) | Abstract `FisheyeProcessor`: output direction grid, polar → normalized `(u, v)`, `remap()`. |
| [processors/](./processors/) | Concrete processors (currently equidistant). |

## `FisheyeProcessorParameters`

- **`camera_hfov` / `camera_vfov`** — Fisheye span used when turning polar radius into image coordinates (default 185° each).
- **`output_hfov`** — Horizontal FOV of the synthetic pinhole view (default 90°). **`output_vfov`** is derived from aspect ratio and `output_hfov`.
- **`output_image_w` / `output_image_h`** — Output size in pixels (default 1280×720).
- **`is_camera_pointing_up`** — Flips the vertical tangent direction grid (`True` by default).
- **`method`** — Selects the processor class via `build_processor()`; only `EQUIDISTANT` is implemented.

## Pipeline (equidistant)

1. Build a grid of unit viewing directions from `output_hfov`, derived `output_vfov`, and output dimensions.
2. Rotate directions with the supplied `RotationMatrix`.
3. Convert directions to polar radius and angle, normalize to fisheye `(u, v)` in \([0, 1]\).
4. Run `cv2.remap` with cubic interpolation.

## Dependencies

- **opencv-contrib-python** — `cv2.remap` and CLI image I/O.
- **numpy** — Arrays throughout.
- **[units](https://github.com/ry-yoshida-private/Units)** — `Angle` for FOV fields.
- **[rotation](https://github.com/ry-yoshida-private/Rotation)** — `RotationMatrix`.
- **[geometry](https://github.com/ry-yoshida-private/Geometry)** — `PolarCoordinate`, `Vectors3D`, and angle helpers on vectors.
