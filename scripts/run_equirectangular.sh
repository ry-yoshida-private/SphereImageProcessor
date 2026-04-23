#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./scripts/run_equirectangular.sh [options]

Options:
  -i, --input PATH               Input equirectangular image path
                                 (default: image/equirectangular.JPG)
  -o, --output PATH              Output image path
                                 (default: tmp_equirectangular_down.jpg)
      --method NAME              Projection method
                                 (perspective)
                                 (default: perspective)
      --camera-pointing-up       Treat camera as pointing upward
      --no-camera-pointing-up    Treat camera as NOT pointing upward
      --yaw-deg FLOAT            Yaw in degrees (default: 0)
      --pitch-deg FLOAT          Pitch in degrees (default: 0)
      --roll-deg FLOAT           Roll in degrees (default: 0)
      --python CMD               Python command (default: python)
  -h, --help                     Show this help

Example:
  ./scripts/run_equirectangular.sh \
    --input image/equirectangular.JPG \
    --output tmp_equirectangular_down.jpg \
    --method perspective \
    --no-camera-pointing-up
EOF
}

INPUT_IMAGE="image/equirectangular.JPG"
OUTPUT_IMAGE="tmp_equirectangular_down.jpg"
METHOD="perspective"
CAMERA_FLAG="--no-camera-pointing-up"
YAW_DEG="0"
PITCH_DEG="0"
ROLL_DEG="0"
PYTHON_CMD="python"

require_value() {
  local option="$1"
  if [[ $# -lt 2 || -z "${2:-}" ]]; then
    echo "Missing value for ${option}" >&2
    usage >&2
    exit 2
  fi
}

validate_method() {
  case "$1" in
    perspective) ;;
    *)
      echo "Invalid --method: $1" >&2
      echo "Allowed: perspective" >&2
      exit 2
      ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -i|--input)
      require_value "$1" "${2:-}"
      INPUT_IMAGE="$2"
      shift 2
      ;;
    -o|--output)
      require_value "$1" "${2:-}"
      OUTPUT_IMAGE="$2"
      shift 2
      ;;
    --method)
      require_value "$1" "${2:-}"
      validate_method "$2"
      METHOD="$2"
      shift 2
      ;;
    --camera-pointing-up)
      CAMERA_FLAG="--camera-pointing-up"
      shift
      ;;
    --no-camera-pointing-up)
      CAMERA_FLAG="--no-camera-pointing-up"
      shift
      ;;
    --yaw-deg)
      require_value "$1" "${2:-}"
      YAW_DEG="$2"
      shift 2
      ;;
    --pitch-deg)
      require_value "$1" "${2:-}"
      PITCH_DEG="$2"
      shift 2
      ;;
    --roll-deg)
      require_value "$1" "${2:-}"
      ROLL_DEG="$2"
      shift 2
      ;;
    --python)
      require_value "$1" "${2:-}"
      PYTHON_CMD="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

cmd=(
  "${PYTHON_CMD}" -m src.sphere_image.equirectangular
  -i "${INPUT_IMAGE}"
  -o "${OUTPUT_IMAGE}"
  --method "${METHOD}"
  "${CAMERA_FLAG}"
  --yaw-deg "${YAW_DEG}"
  --pitch-deg "${PITCH_DEG}"
  --roll-deg "${ROLL_DEG}"
)

"${cmd[@]}"
