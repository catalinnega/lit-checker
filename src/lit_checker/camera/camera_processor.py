import cv2
import numpy as np
import os
from datetime import datetime

from lit_checker.args import GlobalConfig, FilesConfig
from lit_checker.camera.args import CameraConfig
from lit_checker.camera.base_camera import BaseCamera
from lit_checker.logging import get_logger


class CameraProcessor:
    def __init__(self, config: GlobalConfig):
        self.config = config
        self.camera = self.__load_camera(config.camera)
        self.log = get_logger(config.log)

        self.frame_buffer = []
        self.frame_height = 0
        self.frame_width = 0

    def run_capture_routine(self, maximum_frames: int = 0) -> list[np.ndarray]:
        capture = cv2.VideoCapture(self.camera.url)
        frame_width, frame_height = self.__get_frame_specs(capture)
        self.frame_width = frame_width
        self.frame_height = frame_height

        self.log.info(f"Running capture routine..")
        while True:
            ret, frame = capture.read()
            if not ret:
                self.log.warning(
                    f"Frame could not be captured")
                break
            self.frame_buffer.append(frame.copy())
            if maximum_frames and len(self.frame_buffer) >= maximum_frames:
                self.log.info(f"Maximum frames reached: {maximum_frames}")
                break
        self.log.info("Capture complete.")
        return self.frame_buffer

    def write_frames(self, frame_buffer: list[np.ndarray]) -> str:
        if len(frame_buffer):
            output_video_path = self.__get_output_video_path(self.config.files)
            encoder_protocol = self.__get_encoder_protocol_code(
                self.config.files.video_file_extension)
            video_writer = cv2.VideoWriter(output_video_path, encoder_protocol,
                                           self.camera.fps, (self.frame_width, self.frame_height))
            for frame in frame_buffer:
                video_writer.write(frame)
            video_writer.release()
            self.log.info(
                f"Wrote {len(self.frame_buffer)} frames at {output_video_path}")
            cv2.destroyAllWindows()
        else:
            self.log.warning(
                f"Attempted to write empty buffer (length {len(frame_buffer)})")
            output_video_path = ""
        return output_video_path

    def __load_camera(self, config: CameraConfig) -> BaseCamera:
        if config.type == 'c100':
            from lit_checker.camera.c100.c100_camera import C100Camera
            camera = C100Camera(config.c100)
        else:
            self.log.error(
                f"Camera could not be identified with camera type: '{config.type}'.")
            camera = None
        return camera

    def __get_frame_specs(self, cap: cv2.VideoCapture) -> tuple[int, int]:
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return frame_width, frame_height

    def __get_output_video_path(self, config: FilesConfig) -> str:
        date_str = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        output_video_path = os.path.join(
            config.output_dir, f"{config.output_prefix}_{date_str}.{config.video_file_extension}")
        return output_video_path

    def __get_encoder_protocol_code(self, video_file_extension: str) -> int:
        if video_file_extension == 'mp4':
            encoder_protocol_code = cv2.VideoWriter_fourcc(*'mp4v')
        else:
            self.log.error(
                f'Unknown video file extension: {video_file_extension}')
            encoder_protocol_code = -1
        return encoder_protocol_code
