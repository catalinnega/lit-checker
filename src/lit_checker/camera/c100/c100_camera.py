from lit_checker.camera.base_camera import BaseCamera
from lit_checker.camera.c100.args import C100Config


class C100Camera(BaseCamera):
    def __init__(self, config: C100Config):
        super().__init__(config)

    def _get_url(self, camera_config: C100Config) -> str:
        url = f"rtsp://{camera_config.username}:{camera_config.password}@{camera_config.ip_address}:{camera_config.port}/stream2"
        return url
