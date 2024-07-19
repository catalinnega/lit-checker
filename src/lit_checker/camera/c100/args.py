from dataclasses import dataclass, field


@dataclass
class C100Config:
    username: str = field(
        default="your_username",
        metadata={
            "help": "Username for Tapo C100 camera, found in \
                  the Tapo Home app > Advanced Settings > Camera Account."
        },
    )
    password: str = field(
        default="your_pass",
        metadata={
            "help": "Password for Tapo C100 camera, found in \
                the Tapo Home app > Advanced Settings > Camera Account."
        },
    )
    ip_address: str = field(
        default="your_ip",
        metadata={"help": "IP for Tapo C100 camera, found in the Tapo Home app > Device Info."},
    )
    port: int = field(
        default=554,
        metadata={
            "help": "Port used for the camera RSVP communication. \
                For Tapo devices, including C100, it is 554. \
                    Port forwarding should be enabled on router and firewall settings."
        },
    )
    fps: int = field(
        default=15,
        metadata={"help": "Camera recording frames per seconds. For Tapo C100, it is 15."},
    )
