from dataclasses import dataclass, field


@dataclass
class DetectionPersistanceConfig:
    memory_size: int = field(
        default=10,
        metadata={
            "help": "The size of the fixed size FIFO list containing instantaneous detections. \
                Here an instantaneous detection is a boolean value that is positive if the \
                     'motion_min_contour_area' condition is satisfied. \
                This list is will affect the 'detection persistance logic' behind the\
                      motion detection decision"
        },
    )
    activation_detection_ratio_threshold: float = field(
        default=0.0,
        metadata={
            "help": "Used to trigger motion detection. \
                  Represents the minimum ratio between the number of \
                    instantaneous detections and the detection buffer size."
        },
    )
    deactivation_detection_ratio_threshold: float = field(
        default=0.1,
        metadata={
            "help": "Used to invalidate motion detection. \
                  Represents the maximum ratio between the number of \
                    instantaneous detections and the detection buffer size."
        },
    )


@dataclass
class MotionDetectionConfig:
    motion_min_contour_area: int = field(
        default=2500, metadata={"help": "Contour area minimum value for considering motion."}
    )
    warmup_seconds: float = field(
        default=2.0,
        metadata={
            "help": "Number of seconds for motion detector to be warmed up. \
                  Detection will not be triggered during this period"
        },
    )
    detection_persistance: DetectionPersistanceConfig = field(
        default_factory=DetectionPersistanceConfig,
        metadata={
            "help": "Configuration for the 'detection persistance' logic used to \
                        trigger motion detection. \
                  The logic considers motion to be detected if there are \
                    enough positive past instantaneous motion detections. \
                  To track the past instantaneous detections, a fixed-size FIFO buffer is used. \
                  To trigger/deactivate motion detection, we consider the ratio between the \
                    number of positive values within the buffer and the buffer size.\
                  Note that the 'instantaneous detection' does not represent the \
                    final 'motion detection' decision.\
                  "
        },
    )

    def __post_init__(self) -> None:
        self.detection_persistance = DetectionPersistanceConfig(**self.detection_persistance)  # type: ignore
