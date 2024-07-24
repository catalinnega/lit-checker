import logging
from collections import deque
from time import time
from typing import Deque, Dict

import cv2
import numpy as np
from lit_checker.args import FilesConfig
from lit_checker.logging import LogConfig, get_logger
from lit_checker.motion_detection.args import DetectionPersistanceConfig, MotionDetectionConfig

# from lit_checker.motion_detection.background_image_processor import BackgroundImageProcessor
from lit_checker.motion_detection.foreground_image_processor import ForegroundImageProcessor
from numpy.typing import NDArray


class MotionDetector:
    def __init__(
        self,
        motion_detection_config: MotionDetectionConfig,
        files_config: FilesConfig,
        camera_url: str,
        logger: logging.Logger | None,
        verbose: bool = False,
    ):
        if logger is not None:
            self.log = logger
        else:
            self.log = get_logger(LogConfig())
        self.motion_detection_config = motion_detection_config
        self.files_config = files_config
        self.detection_persistance_config: DetectionPersistanceConfig = (
            self.motion_detection_config.detection_persistance
        )

        self.current_motion_feature_dict = self.__init_current_motion_feature_dict()

        # self.background_image = BackgroundImageProcessor(
        #     config=files_config, camera_url=camera_url, logger=self.log, verbose=verbose
        # )

        self.foreground_processor = ForegroundImageProcessor(
            config=files_config, logger=self.log, verbose=verbose
        )
        self.motion_detected = False
        self.start_time: None | float = None

    def apply(self, current_frame: NDArray[np.uint8]) -> tuple[bool, bool]:
        foreground_frame = self.__apply_background_subtractor(current_frame)
        if self.__is_motion_detection_ready():
            foreground_frame = self.foreground_processor.apply_foreground_post_processing(
                foreground_frame
            )
            contours = self.foreground_processor.find_contours(foreground_frame)
            motion_detected, motion_detection_changed = self.decide_motion_by_contour_areas(
                contours
            )
            if motion_detection_changed:
                if motion_detected:
                    self.log.info("Motion detected")
                    self.foreground_processor.plot_contour(current_frame, contours)
                else:
                    self.log.info("Motion stopped")
        else:
            motion_detection_changed = False
            motion_detected = False

        self.motion_detected = motion_detected
        return motion_detected, motion_detection_changed

    def decide_motion_by_contour_areas(
        self, contours: list[NDArray[np.int32]]
    ) -> tuple[bool, bool]:
        is_area_over_thr = False
        for contour in contours:
            area_value = cv2.contourArea(contour)
            is_area_over_thr = area_value > self.motion_detection_config.motion_min_contour_area
            if is_area_over_thr:
                break

        motion_detected = self.__apply_motion_detection_decision(
            is_area_over_min_thr=is_area_over_thr,
            current_motion_feature_dict=self.current_motion_feature_dict,
        )
        motion_detection_changed = (
            motion_detected != self.current_motion_feature_dict["motion_detection"]
        )

        self.current_motion_feature_dict = self.__update_current_motion_dict(
            motion_detection=motion_detected, is_area_over_min_thr=is_area_over_thr
        )
        return motion_detected, motion_detection_changed

    def __apply_motion_detection_decision(
        self,
        is_area_over_min_thr: bool,
        current_motion_feature_dict: Dict[str, bool | Deque[bool]],
    ) -> bool:
        if isinstance(current_motion_feature_dict["detection_persistance_buffer"], Deque):
            detections_buffer = current_motion_feature_dict["detection_persistance_buffer"]
            detections_buffer.append(is_area_over_min_thr)
        else:
            detections_buffer = deque()

        if isinstance(current_motion_feature_dict["motion_detection"], bool):
            motion_detection: bool = current_motion_feature_dict["motion_detection"]
        else:
            motion_detection = False

        config = self.detection_persistance_config
        detection_percentage = sum(detections_buffer) / len(detections_buffer)
        if detection_percentage > config.activation_detection_ratio_threshold:
            motion_detection = True
        elif detection_percentage < config.deactivation_detection_ratio_threshold:
            motion_detection = False
        return motion_detection

    def __update_current_motion_dict(
        self, motion_detection: bool, is_area_over_min_thr: bool
    ) -> Dict[str, bool | Deque[bool]]:
        motion_dict = self.current_motion_feature_dict
        motion_dict["motion_detection"] = motion_detection

        if isinstance(motion_dict["detection_persistance_buffer"], Deque):
            motion_dict["detection_persistance_buffer"].append(is_area_over_min_thr)
        return motion_dict

    def __is_motion_detection_ready(self) -> bool:
        if self.start_time is None:
            self.start_time = time()

        is_motion_detection_ready = False
        if self.start_time is not None:
            start_time: float = self.start_time
            if time() - start_time > self.motion_detection_config.warmup_seconds:
                is_motion_detection_ready = True
            else:
                is_motion_detection_ready = False
        return is_motion_detection_ready

    def __apply_background_subtractor(self, frame: NDArray[np.uint8]) -> NDArray[np.uint8]:
        frame_cv2 = self.foreground_processor.apply_background_subtractor_on_frame(
            frame, self.motion_detected
        )
        frame = np.array(frame_cv2, dtype=np.uint8)
        return frame

    def __init_current_motion_feature_dict(self) -> Dict[str, bool | Deque[bool]]:
        buffer: Deque[bool] = deque(maxlen=self.detection_persistance_config.memory_size)
        motion_dict: Dict[str, bool | Deque[bool]] = {
            "motion_detection": False,
            "detection_persistance_buffer": buffer,
        }
        return motion_dict
