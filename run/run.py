import argparse

from lit_checker.args import GlobalConfig
from lit_checker.camera.camera_processor import CameraProcessor


def main(yaml_config_path: str) -> None:
    config = GlobalConfig.from_yaml(yaml_config_path)
    camera_processor = CameraProcessor(config, verbose=False)

    # this will run indefinetly until interruption:
    _ = camera_processor.run_capture_routine()


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
