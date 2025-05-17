import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union


class Logger:
    def __init__(self,
                 name: str,
                 file_name: str,
                 max_bytes: int,
                 backup_count: int,
                 level: int = logging.INFO):
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(level)

        Path("logs").mkdir(exist_ok=True)
        log_file_path: Path = Path("logs") / file_name

        self.file_handler: RotatingFileHandler = RotatingFileHandler(
            log_file_path, maxBytes=max_bytes, backupCount=backup_count
        )
        formatter: logging.Formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.file_handler.setFormatter(formatter)

        self.logger.addHandler(self.file_handler)

    def get_logger(self) -> logging.Logger:
        return self.logger
