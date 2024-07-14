from dataclasses import dataclass, field
import yaml
from lit_checker.camera.args import CameraConfig
from lit_checker.logging import LogConfig


@dataclass
class FilesConfig:
    output_dir: str = field(
        default='out',
        metadata={
            "help": "Output directory path"
        })
    output_prefix: str = field(
        default='test',
        metadata={
            "help": "Output filename prefix"
        })
    video_file_extension: str = field(
        default='mp4',
        metadata={
            "help": "Video file extension"
        })


@dataclass
class GlobalConfig:
    camera: CameraConfig = field(
        default_factory=CameraConfig,
        metadata={
            "help": "Camera config"
        }
    )
    files: FilesConfig = field(
        default_factory=FilesConfig,
        metadata={
            "help": "Files config"
        }
    )
    log: LogConfig = field(
        default_factory=LogConfig,
        metadata={
            "help": "Logging config"
        }
    )

    def __post_init__(self):
        self.files = FilesConfig(**self.files)
        self.camera = CameraConfig(**self.camera)
        self.log = LogConfig(**self.log)

    @staticmethod
    def from_yaml(yaml_config_path: str):
        with open(yaml_config_path, 'rb') as r:
            cfg = yaml.safe_load(r)
        config = GlobalConfig(**cfg)
        return config
