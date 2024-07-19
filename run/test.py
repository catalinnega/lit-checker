
import cv2
from datetime import datetime
import os
import argparse

from lit_checker.args import GlobalConfig
from lit_checker.camera.camera_processor import CameraProcessor


def main(yaml_config_path: str) -> None:
    config = GlobalConfig.from_yaml(yaml_config_path)
    camera_processor = CameraProcessor(config, verbose=False)
    frames = camera_processor.run_capture_routine(maximum_frames=100)
    output_path = camera_processor.write_frames(frames)
    print(f"Wrote frames at: {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cfg",
        default="configs/c100/config_c100.yaml",
        action="store",
        type=str,
        required=True,
        help="YAML configuration file path")
    args = parser.parse_args()
    main(args.cfg)
