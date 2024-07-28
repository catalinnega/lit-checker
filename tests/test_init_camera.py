import pytest
from lit_checker.args import GlobalConfig
from lit_checker.camera.camera_processor import CameraProcessor


def test_init_camera(yaml_config_path: str) -> None:
    config = GlobalConfig.from_yaml(yaml_config_path)
    camera_processor = CameraProcessor(config, verbose=False)
    assert camera_processor is not None, "Failed to build CameraProcessor"


@pytest.fixture # type: ignore
def yaml_config_path() -> str:
    return "configs/c100/config_c100.yaml"
