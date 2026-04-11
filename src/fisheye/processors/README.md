# processors

## Overview

Concrete fisheye projection models. Each subclass of `FisheyeProcessor` implements `_map_rotation_to_uv()` for its optical model.

## Components

| Component | Description |
| --- | --- |
| [equidistant.py](./equidistant.py) | `EquidistantFisheyeProcessor`: equidistant fisheye model; includes a `main()` CLI. |

## Equidistant processor

Directions from the abstract base class are expressed in camera coordinates, rotated by `RotationMatrix`, then converted to azimuthal and polar angles. Radius is scaled by `camera_hfov`; the result is written as a `PolarCoordinate` and projected to normalized image `(u, v)` for `remap()`.

## CLI (`equidistant`)

Run as a module from any working directory after the package is installed:

```bash
python -m fisheye.processors.equidistant -i in.jpg -o out.jpg
```

Options:

- **`-i` / `--input`** — Input fisheye image (default `data/input_fisheye.jpg`).
- **`-o` / `--output`** — Output path (default `tmp_fisheye.jpg`).
- **`--camera-pointing-up` / `--no-camera-pointing-up`** — Override `FisheyeProcessorParameters.is_camera_pointing_up` when set; otherwise parameters use their defaults.
