# processors

## Overview

Concrete fisheye projection models. Each subclass of `FisheyeProcessor` implements `_map_rotation_to_uv()` for its optical model.

## Components

| Component | Description |
| --- | --- |
| [equidistant.py](./equidistant.py) | `EquidistantFisheyeProcessor`: equidistant fisheye model; includes a `main()` CLI. |
| [orthographic.py](./orthographic.py) | `OrthographicFisheyeProcessor`: orthographic fisheye model. |
| [stereographic.py](./stereographic.py) | `StereographicFisheyeProcessor`: stereographic fisheye model. |
| [equisolid.py](./equisolid.py) | `EquisolidFisheyeProcessor`: equisolid-angle fisheye model. |
| [utils/](./utils/) | Small helpers used by processor CLIs (argument parsing, I/O, rotation construction). |

## Radius models

Directions from the abstract base class are expressed in camera coordinates, rotated by `RotationMatrix`, then converted to azimuthal and polar angles. Radius is normalized by the maximum incident angle $\theta_{\max} = \frac{\mathrm{camera\_hfov}}{2}$:

| Model | Radius equation |
| --- | --- |
| Equidistant | $r = \frac{\theta}{\theta_{\max}}$ |
| Orthographic | $r = \frac{\sin(\theta)}{\sin(\theta_{\max})}$ |
| Stereographic | $r = \frac{\tan(\theta/2)}{\tan(\theta_{\max}/2)}$ |
| Equisolid | $r = \frac{\sin(\theta/2)}{\sin(\theta_{\max}/2)}$ |

The resulting `PolarCoordinate` is projected to normalized image `(u, v)` for `remap()`.

## CLI

Use this script for day-to-day execution.

### Script usage

Run one method with explicit options:

```bash
./scripts/run_fisheye.sh \
  --input image/input_fisheye.jpg \
  --output tmp_fisheye_down.jpg \
  --method stereographic \
  --yaw-deg 5 \
  --pitch-deg -3 \
  --roll-deg 1 \
  --no-camera-pointing-up
```

### Options

| Option | Description |
| --- | --- |
| `-i`, `--input` | Input fisheye image path (default: `image/input_fisheye.jpg`). |
| `-o`, `--output` | Output image path (default: `tmp_fisheye_down.jpg`). |
| `--method` | Method to run: `equidistant`, `orthographic`, `stereographic`, `equisolid`. |
| `--camera-pointing-up`, `--no-camera-pointing-up` | Override camera vertical orientation. |
| `--yaw-deg` | Yaw angle in degrees. |
| `--pitch-deg` | Pitch angle in degrees. |
| `--roll-deg` | Roll angle in degrees. |

For complete script usage:

```bash
./scripts/run_fisheye.sh --help
```
