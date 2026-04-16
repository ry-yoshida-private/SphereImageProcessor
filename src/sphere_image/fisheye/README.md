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
| `camera_hfov` / `camera_vfov` | Fisheye span used when turning polar radius into image coordinates (default 185° each). |
| `output_hfov` | Horizontal FOV of the synthetic pinhole view (default 90°). `output_vfov` is derived from aspect ratio and `output_hfov`. |
| `output_image_w` / `output_image_h` | Output size in pixels (default 1280x720). |
| `is_camera_pointing_up` | Flips the vertical tangent direction grid (`True` by default). |
| `method` | Selects the processor class via `build_processor()` (`EQUIDISTANT`, `ORTHOGRAPHIC`, `STEREOGRAPHIC`, `EQUISOLID`). |

