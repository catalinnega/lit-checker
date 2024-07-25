from dataclasses import dataclass, field
from typing import Any

import yaml

from lit_checker.camera.args import CameraConfig
from lit_checker.drive.args import GoogleDriveUploaderConfig
from lit_checker.logging import LogConfig
from lit_checker.mail.args import MailServiceConfig
from lit_checker.motion_detection.args import MotionDetectionConfig


@dataclass
class FilesConfig:
    output_dir: str = field(default="out", metadata={
                            "help": "Output directory path"})
    output_prefix: str = field(default="test", metadata={
                               "help": "Output filename prefix"})
    video_file_extension: str = field(
        default="mp4", metadata={"help": "Video file extension"})
    background_image_fname: str = field(
        default="background.jpg",
        metadata={
            "help": "Background image file name. \
                Will be saved in 'output_dir' directory."
        },
    )


@dataclass
class GlobalConfig:
    camera: CameraConfig = field(default_factory=CameraConfig, metadata={
                                 "help": "Camera config"})
    files: FilesConfig = field(default_factory=FilesConfig, metadata={
                               "help": "Files config"})
    log: LogConfig = field(default_factory=LogConfig,
                           metadata={"help": "Logging config"})
    motion_detection: MotionDetectionConfig = field(
        default_factory=MotionDetectionConfig, metadata={
            "help": "Motion detection config"}
    )
    drive: GoogleDriveUploaderConfig = field(
        default_factory=GoogleDriveUploaderConfig, metadata={
            "help": "Google Drive uploader config"}
    )
    mail: MailServiceConfig = field(
        default_factory=MailServiceConfig, metadata={
            "help": "Mail service config"}
    )

    def __post_init__(self) -> None:
        self.files = FilesConfig(**self.files)  # type: ignore
        self.camera = CameraConfig(**self.camera)  # type: ignore
        self.log = LogConfig(**self.log)  # type: ignore
        self.motion_detection = MotionDetectionConfig(
            **self.motion_detection)  # type: ignore
        self.drive = GoogleDriveUploaderConfig(**self.drive)  # type: ignore
        self.mail = MailServiceConfig(**self.mail)  # type: ignore

    @staticmethod
    def from_yaml(yaml_config_path: str) -> Any:
        with open(yaml_config_path, "rb") as r:
            cfg = yaml.safe_load(r)
        config = GlobalConfig(**cfg)
        return config
