import logging
import logging.handlers
import os
import sys
from dataclasses import dataclass, field


@dataclass
class LogConfig:
    level: str = field(default="info", metadata={"help": "logging level type"})
    name: str = field(default="main", metadata={"help": "Logger name"})
    log_file_name: str = field(default="log.txt", metadata={
                               "help": "Log file name"})


def get_logger(log_config: LogConfig, output_directory: str = 'out') -> logging.Logger:
    output_directory = os.path.join(output_directory, 'logs')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    logging_level = get_logging_level(log_config)
    formatter = get_formatter()

    logger = logging.getLogger(log_config.name)
    logger.setLevel(logging_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    output_path = os.path.join(output_directory, log_config.log_file_name)
    file_handler = logging.handlers.TimedRotatingFileHandler(
        output_path,
        when="D",
        interval=1,
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.info("Initialized logger.")
    return logger


def get_formatter() -> logging.Formatter:
    return logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def get_logging_level(log_config: LogConfig) -> str:
    log_level_setting = log_config.level.upper()
    if log_level_setting not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
        log_level_setting = "DEBUG"
    logging_level: str = getattr(logging, log_config.level.upper())
    return logging_level
