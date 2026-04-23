# fisheye

## Overview

This package maps fisheye input to a pinhole-like image by sampling the fisheye texture along rays derived from output FOV and an optional world rotation. Shared logic lives on `FisheyeProcessor`; projection-specific radius equations are selected by `FisheyeProjectionMethod`.

Implemented projection models: `EQUIDISTANT`, `ORTHOGRAPHIC`, `STEREOGRAPHIC`, and `EQUISOLID`.

## Components

| Component | Description |
| --- | --- |
| [parameter.py](./parameter.py) | `FisheyeProcessorParameters` (FOV, resolution, method, vertical flip) and `build_processor()`. |
| [method.py](./method.py) | `FisheyeProjectionMethod` enum and per-model radius equation (`calculate_radius`). |
| [processor.py](./processor.py) | `FisheyeProcessor` unified implementation: direction grid, polar → normalized `(u, v)`, `remap()`. |

## `FisheyeProcessorParameters`

| Parameter | Description |
| --- | --- |
| `camera_fov` | Circular fisheye span used when turning polar radius into image coordinates. |
| `output_fov` / `output_basis` | Base output FOV and its axis (`VERTICAL` or `HORIZONTAL`). `output_hfov` and `output_vfov` are derived from these values and aspect ratio. |
| `output_image_w` / `output_image_h` | Output size in pixels. |
| `is_camera_pointing_up` | Whether to flip the vertical tangent direction grid. |
| `method` | Selects the processor class via `build_processor()` (`EQUIDISTANT`, `ORTHOGRAPHIC`, `STEREOGRAPHIC`, `EQUISOLID`). |

