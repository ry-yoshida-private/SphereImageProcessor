# FisheyeImage

FisheyeImage is a Python package for remapping fisheye images toward a rectilinear-style view. It uses an equidistant projection model, builds per-pixel sampling coordinates with NumPy, and warps with `cv2.remap`. Field of view and output resolution are configured through `FisheyeProcessorParameters`.

For module-level detail, see [src/fisheye/README.md](src/fisheye/README.md).

## Installation

From the package root (the directory containing `pyproject.toml`):

```bash
pip install .
```

For development, install in editable mode:

```bash
pip install -e .
```

Dependencies are installed automatically. To install dependencies only:

```bash
pip install -r requirements.txt
```

## Example

```python
import cv2
from rotation import RotationMatrix

from fisheye.parameter import FisheyeProcessorParameters
from fisheye.processors import EquidistantFisheyeProcessor

image = cv2.imread("input.jpg")
params = FisheyeProcessorParameters()
processor = EquidistantFisheyeProcessor(image=image, params=params)
out = processor.run_pipeline(rotation_matrix=RotationMatrix.unit_matrix())
```

A small CLI lives in `fisheye.processors.equidistant`; see [src/fisheye/processors/README.md](src/fisheye/processors/README.md).
