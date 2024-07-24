import logging
import os

import cv2
import numpy as np
from lit_checker.args import FilesConfig
from lit_checker.logging import LogConfig, get_logger
from numpy.typing import NDArray


class ForegroundImageProcessor:
    def __init__(self, config: FilesConfig, logger: logging.Logger | None, verbose: bool = False):
        if logger is not None:
            self.log = logger
        else:
            self.log = get_logger(LogConfig())
        self.config = config
        self.background_subtractor = self.__init_background_subtractor()
        self.verbose = verbose

    def apply_background_subtractor_on_frame(
            self,
            frame: NDArray[np.uint8],
            motion_detected: bool = False) -> NDArray[np.uint8]:
        learning_rate = 0.0 if motion_detected else -1.0
        frame_cv2 = self.background_subtractor.apply(
            frame, learningRate=learning_rate)
        frame = np.array(frame_cv2, dtype=np.uint8)
        return frame

    def subtract_background(
        self,
        current_frame: NDArray[np.uint8],
        background_frame: NDArray[np.uint8],
        postprocess_foreground: bool = True,
    ) -> NDArray[np.uint8]:
        added_frame = self.__get_added_frame(current_frame, background_frame)
        foreground_frame = self.__apply_background_subtractor(added_frame)

        if postprocess_foreground:
            foreground_frame_postprocessed = self.apply_foreground_post_processing(
                foreground_frame
            )
        else:
            foreground_frame_postprocessed = foreground_frame

        if self.verbose:
            _ = self.__log_background_images(
                current_frame=current_frame,
                added_frame=added_frame,
                foreground_frame=foreground_frame,
                foreground_frame_postprocessed=foreground_frame_postprocessed,
                output_dir=self.config.output_dir,
                output_fname_prefix=self.config.output_prefix,
            )
        return foreground_frame

    def find_contours(self, foreground_frame: NDArray[np.uint8]) -> list[NDArray[np.int32]]:
        found_contours, _ = cv2.findContours(
            foreground_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contours: list[NDArray[np.int32]] = [
            np.array(contour, dtype=np.int32) for contour in found_contours
        ]
        return contours

    def apply_foreground_post_processing(
        self, foreground_frame: NDArray[np.uint8]
    ) -> NDArray[np.uint8]:
        _, binary_mask = cv2.threshold(
            foreground_frame, 200, 255, cv2.THRESH_BINARY)
        kernel = np.ones((5, 5), np.uint8)
        clean_mask_cv2 = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)
        clean_mask_cv2 = cv2.morphologyEx(
            clean_mask_cv2, cv2.MORPH_OPEN, kernel)
        clean_mask = np.array(clean_mask_cv2, dtype=np.uint8)
        return clean_mask

    def plot_contour(
        self, current_frame: NDArray[np.uint8], contours: list[NDArray[np.int32]]
    ) -> str:
        local_output_dir = os.path.join(self.config.output_dir, "contours")
        if not os.path.exists(local_output_dir):
            os.makedirs(local_output_dir)
            self.log.info(f"Created directory at: {local_output_dir}")
        foreground_frame_copy = current_frame.copy()
        output_path = os.path.join(local_output_dir, "contour_add.jpg")
        cv2.drawContours(foreground_frame_copy, contours, -1, (0, 255, 0), 2)
        cv2.imwrite(output_path, foreground_frame_copy)
        self.log.info(f"Wrote added image at {output_path}")
        return output_path

    def __apply_background_subtractor(self, frame: NDArray[np.uint8]) -> NDArray[np.uint8]:
        frame_cv2 = self.background_subtractor.apply(frame)
        frame = np.array(frame_cv2, dtype=np.uint8)
        return frame

    def __get_added_frame(
        self, current_frame: NDArray[np.uint8], background_frame: NDArray[np.uint8]
    ) -> NDArray[np.uint8]:
        added_frame_cv2 = cv2.bitwise_and(current_frame, background_frame)
        added_frame = np.array(added_frame_cv2, dtype=np.uint8)
        return added_frame

    def __log_background_images(
        self,
        current_frame: NDArray[np.uint8],
        added_frame: NDArray[np.uint8],
        foreground_frame: NDArray[np.uint8],
        foreground_frame_postprocessed: NDArray[np.uint8],
        output_dir: str,
        output_fname_prefix: str,
    ) -> str:
        local_output_dir = os.path.join(self.config.output_dir, "foreground")
        if not os.path.exists(local_output_dir):
            os.makedirs(local_output_dir)
            self.log.info(f"Created directory at: {local_output_dir}")

        output_path = os.path.join(
            local_output_dir, f"{output_fname_prefix}_current.jpg")
        cv2.imwrite(output_path, current_frame)
        self.log.info(f"Wrote added image at {output_path}")

        output_path = os.path.join(
            local_output_dir, f"{output_fname_prefix}_add.jpg")
        cv2.imwrite(output_path, added_frame)
        self.log.info(f"Wrote added image at {output_path}")

        output_path = os.path.join(
            local_output_dir, f"{output_fname_prefix}_foreground.jpg")
        cv2.imwrite(output_path, foreground_frame)
        self.log.info(f"Wrote foreground image at {output_path}")

        output_path = os.path.join(
            local_output_dir, f"{output_fname_prefix}_foreground_postprocessed.jpg"
        )
        cv2.imwrite(output_path, foreground_frame_postprocessed)
        self.log.info(f"Wrote foreground image at {output_path}")
        return output_dir

    def __init_background_subtractor(self) -> cv2.BackgroundSubtractorMOG2:
        return cv2.createBackgroundSubtractorMOG2(
            detectShadows=False, history=100, varThreshold=100
        )
