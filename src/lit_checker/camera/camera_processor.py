import logging
import os
from datetime import datetime

import cv2
import numpy as np
from cv2 import VideoWriter_fourcc  # type: ignore
from lit_checker.args import FilesConfig, GlobalConfig
from lit_checker.camera.args import CameraConfig
from lit_checker.camera.base_camera import BaseCamera
from lit_checker.camera.exceptions import InvalidCameraTypeException
from lit_checker.drive.args import GoogleDriveUploaderConfig
from lit_checker.drive.google_drive_uploader import GoogleDriveUploader
from lit_checker.logging import get_logger
from lit_checker.mail.args import MailServiceConfig
from lit_checker.motion_detection.motion_detector import MotionDetector
from numpy.typing import NDArray


class CameraProcessor:
    def __init__(self, config: GlobalConfig, verbose: bool = False):
        self.config = config
        self.camera = self.__load_camera(config.camera)
        self.log = get_logger(config.log, config.files.output_dir)

        self.motion_detector = MotionDetector(
            config.motion_detection,
            files_config=config.files,
            camera_url=self.camera.url,
            logger=self.log,
        )

        self.google_drive_uploader = self.__init_google_drive_uploader(
            drive_config=config.drive, mail_config=config.mail, logger=self.log
        )

        self.frame_buffer: list[NDArray[np.uint8]] = []
        self.frame_height = 0
        self.frame_width = 0

    def run_capture_routine(self, maximum_frames: int = 0) -> list[NDArray[np.uint8]]:
        capture = cv2.VideoCapture(self.camera.url)
        frame_width, frame_height = self.__get_frame_specs(capture)
        self.frame_width = frame_width
        self.frame_height = frame_height

        motion_detected = False
        self.log.info("Running capture routine..")
        while True:
            are_frames, frame = self.__read_frame(capture)
            if not are_frames:
                self.log.warning("Frame could not be captured")
                break

            motion_detected, motion_detection_changed = self.motion_detector.apply(
                frame)
            if motion_detected:
                self.frame_buffer.append(frame)
            elif motion_detection_changed:
                if len(self.frame_buffer) >= self.config.camera.minimum_write_frames:
                    self.write_frames(self.frame_buffer)
                self.frame_buffer = []
            if maximum_frames and len(self.frame_buffer) >= maximum_frames:
                self.log.info(f"Maximum frames reached: {maximum_frames}")
                break
        self.log.info("Capture complete.")
        return self.frame_buffer

    def write_frames(self, frame_buffer: list[NDArray[np.uint8]]) -> str:
        if len(frame_buffer):
            output_video_path = self.__get_output_video_path(self.config.files)
            encoder_protocol = self.__get_encoder_protocol_code(
                self.config.files.video_file_extension
            )
            video_writer = cv2.VideoWriter(
                output_video_path,
                encoder_protocol,
                self.camera.fps,
                (self.frame_width, self.frame_height),
            )
            for frame in frame_buffer:
                video_writer.write(frame)
            video_writer.release()
            self.log.info(
                f"Wrote {len(self.frame_buffer)} frames at {output_video_path}")
            if self.google_drive_uploader is not None:
                self.google_drive_uploader.upload_file_to_folder(
                    file_path=output_video_path, folder_name="motion_detections"
                )
        else:
            self.log.warning(
                f"Attempted to write empty buffer (length {len(frame_buffer)})")
            output_video_path = ""
        return output_video_path

    def __read_frame(self, capture: cv2.VideoCapture) -> tuple[bool, NDArray[np.uint8]]:
        are_frames, frame_cv2 = capture.read()
        frame = np.array(frame_cv2, dtype=np.uint8)
        return are_frames, frame

    def __load_camera(self, config: CameraConfig) -> BaseCamera:
        if config.type == "c100":
            from lit_checker.camera.c100.c100_camera import C100Camera

            camera = C100Camera(config.c100)
            return camera
        else:
            self.log.error(
                f"Camera could not be identified with camera type: '{config.type}'.")
            raise InvalidCameraTypeException(
                f"Invalid camera type: {config.type}")

    def __get_frame_specs(self, cap: cv2.VideoCapture) -> tuple[int, int]:
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return frame_width, frame_height

    def __get_output_video_path(self, config: FilesConfig) -> str:
        date_str = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        output_video_path = os.path.join(
            config.output_dir, f"{config.output_prefix}_{date_str}.{config.video_file_extension}"
        )
        return output_video_path

    def __get_encoder_protocol_code(self, video_file_extension: str) -> int:
        if video_file_extension == "mp4":
            encoder_protocol_code: int = VideoWriter_fourcc(*"mp4v")
        else:
            self.log.error(
                f"Unknown video file extension: {video_file_extension}")
            encoder_protocol_code = -1
        return encoder_protocol_code

    def __init_google_drive_uploader(
        self,
        drive_config: GoogleDriveUploaderConfig,
        mail_config: MailServiceConfig,
        logger: logging.Logger,
    ) -> GoogleDriveUploader | None:
        if drive_config.enabled:
            google_drive_uploader = GoogleDriveUploader(
                drive_config, mail_config, logger=logger)
        else:
            google_drive_uploader = None
        return google_drive_uploader
