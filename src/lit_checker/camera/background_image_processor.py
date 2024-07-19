import logging
import os

import cv2
import numpy as np
from lit_checker.args import FilesConfig
from lit_checker.logging import LogConfig, get_logger
from numpy.typing import NDArray


class BackgroundImageProcessor:
    def __init__(
            self,
            config: FilesConfig,
            camera_url: str,
            logger: logging.Logger | None,
            verbose: bool = False):
        if logger is not None:
            self.log = logger
        else:
            self.log = get_logger(LogConfig())
        self.config = config
        self.camera_url = camera_url
        self.background_image_path = self.__get_background_image_path(config)
        self.background_image_frame = self.__get_background_image_frame(
            self.background_image_path, self.camera_url)
        self.verbose = verbose

    def __get_background_image_frame(
            self,
            background_image_path: str,
            camera_url: str) -> NDArray[np.int_]:
        if not os.path.exists(background_image_path):
            background_image = self.__capture_background_image(
                camera_url,
                background_image_path)
        else:
            background_image = self.__load_background_image(
                background_image_path)
        return background_image

    def __load_background_image(self, background_image_path: str) -> NDArray[np.int_]:
        cv2_frame = cv2.imread(background_image_path)
        frame = np.array(cv2_frame, dtype=np.int_)
        self.log.info(f"Loaded background frame from {background_image_path}")
        return frame

    def __capture_background_image(self, url: str, background_image_path: str) -> NDArray[np.int_]:
        capture = cv2.VideoCapture(url)
        are_frames, cv2_frame = capture.read()
        if not are_frames:
            self.log.error(
                "Frame could not be captured for background image")
            frame = np.array([], dtype=np.int_)
        else:
            frame = np.array(cv2_frame, dtype=np.int_)
            cv2.imwrite(background_image_path, frame)
            self.log.info(f"Wrote background image at {background_image_path}")
        return frame

    def __get_background_image_path(self, config: FilesConfig) -> str:
        return os.path.join(
            config.output_dir, config.background_image_fname)
