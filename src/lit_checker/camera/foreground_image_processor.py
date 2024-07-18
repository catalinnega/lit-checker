import cv2
import os
import numpy as np
import logging

from lit_checker.args import FilesConfig
from lit_checker.logging import get_logger, LogConfig


class ForegroundImageProcessor:
    def __init__(self, config: FilesConfig, logger: logging.Logger | None, verbose: bool = False):
        if logger is not None:
            self.log = logger
        else:
            self.log = get_logger(LogConfig())
        self.config = config
        self.background_subtractor = self.__init_background_subtractor()
        self.verbose = verbose

    def subtract_background(
            self,
            current_frame: np.ndarray,
            background_frame: np.ndarray,
            postprocess_foreground: bool = True):
        added_frame = cv2.bitwise_and(current_frame, background_frame)
        foreground_frame = self.background_subtractor.apply(added_frame)

        if postprocess_foreground:
            foreground_frame_postprocessed = self.apply_foreground_post_processing(
                foreground_frame)
        else:
            foreground_frame_postprocessed = foreground_frame

        if self.verbose:
            _ = self.__log_background_images(
                current_frame=current_frame,
                added_frame=added_frame,
                foreground_frame=foreground_frame,
                foreground_frame_postprocessed=foreground_frame_postprocessed,
                output_dir=self.config.output_dir,
                output_fname_prefix=self.config.output_prefix)
        return foreground_frame

    def find_contours(self, foreground_frame: np.ndarray) -> list[np.ndarray]:
        contours, _ = cv2.findContours(
            foreground_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def apply_foreground_post_processing(self, foreground_frame: np.ndarray) -> np.ndarray:
        _, binary_mask = cv2.threshold(
            foreground_frame, 200, 255, cv2.THRESH_BINARY)
        kernel = np.ones((5, 5), np.uint8)
        clean_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)
        clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_OPEN, kernel)
        return clean_mask

    def plot_contour(self, current_frame: np.ndarray, contours: list[np.ndarray]) -> str:
        local_output_dir = os.path.join(self.config.output_dir, 'contours')
        if not os.path.exists(local_output_dir):
            os.makedirs(local_output_dir)
            self.log.info(f"Created directory at: {local_output_dir}")
        foreground_frame_copy = current_frame.copy()
        output_path = os.path.join(
            local_output_dir, f'contour_add.jpg')
        cv2.drawContours(foreground_frame_copy,
                         contours, -1, (0, 255, 0), 2)
        cv2.imwrite(output_path, foreground_frame_copy)
        self.log.info(f"Wrote added image at {output_path}")
        return output_path

    def __log_background_images(
            self,
            current_frame: np.ndarray,
            added_frame: np.ndarray,
            foreground_frame: np.ndarray,
            foreground_frame_postprocessed: np.ndarray,
            output_dir: str,
            output_fname_prefix: str) -> str:
        local_output_dir = os.path.join(self.config.output_dir, 'foreground')
        if not os.path.exists(local_output_dir):
            os.makedirs(local_output_dir)
            self.log.info(f"Created directory at: {local_output_dir}")

        output_path = os.path.join(
            local_output_dir, f'{output_fname_prefix}_current.jpg')
        cv2.imwrite(output_path, current_frame)
        self.log.info(f"Wrote added image at {output_path}")

        output_path = os.path.join(
            local_output_dir, f'{output_fname_prefix}_add.jpg')
        cv2.imwrite(output_path, added_frame)
        self.log.info(f"Wrote added image at {output_path}")

        output_path = os.path.join(
            local_output_dir, f'{output_fname_prefix}_foreground.jpg')
        cv2.imwrite(output_path, foreground_frame)
        self.log.info(f"Wrote foreground image at {output_path}")

        output_path = os.path.join(
            local_output_dir, f'{output_fname_prefix}_foreground_postprocessed.jpg')
        cv2.imwrite(output_path, foreground_frame_postprocessed)
        self.log.info(f"Wrote foreground image at {output_path}")
        return output_dir

    def __init_background_subtractor(self) -> cv2.createBackgroundSubtractorMOG2:
        return cv2.createBackgroundSubtractorMOG2(
            detectShadows=False,
            history=100,
            varThreshold=100
        )
