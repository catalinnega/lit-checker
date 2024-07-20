import argparse

import cv2
import numpy as np
from lit_checker.args import GlobalConfig
from lit_checker.camera.camera_processor import CameraProcessor


def main(yaml_config_path: str) -> None:
    config = GlobalConfig.from_yaml(yaml_config_path)
    camera_processor = CameraProcessor(config, verbose=False)
    capture = cv2.VideoCapture(camera_processor.camera.url)
    _, frame_cv2 = capture.read()
    frame_cv2 = np.array(frame_cv2, dtype=np.uint8)
    _, binary_mask = cv2.threshold(frame_cv2, 200, 255, cv2.THRESH_BINARY)
    camera_processor.log.info(f"ok {binary_mask}")
    camera_processor.log.info(f"ok {frame_cv2.dtype}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cfg",
        default="configs/c100/config_c100.yaml",
        action="store",
        type=str,
        required=True,
        help="YAML configuration file path",
    )
    args = parser.parse_args()
    main(args.cfg)
