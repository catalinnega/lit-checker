from dataclasses import dataclass, field
from lit_checker.camera.c100.args import C100Config


@dataclass
class CameraConfig:
    type: str = field(
        default='c100',
        metadata={
            "help": "camera type ID"
        })
    c100: C100Config = field(
        default_factory=C100Config,
        metadata={
            "help": "Tapo C100 camera config"
        }
    )

    def __post_init__(self):
        self.c100 = C100Config(**self.c100)
