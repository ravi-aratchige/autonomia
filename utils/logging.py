import os
import logging
from datetime import datetime


class ApplicationLogger:
    _logger = None

    @staticmethod
    def get_logger():
        if ApplicationLogger._logger is None:
            # Create logs directory relative to this file
            log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
            os.makedirs(log_dir, exist_ok=True)

            # Create logger
            logger = logging.getLogger("ApplicationLogger")
            logger.setLevel(logging.DEBUG)

            # Define custom logging level (START)

            logging.addLevelName(15, "START")

            def start(self, message, *args, **kwargs):
                if self.isEnabledFor(15):
                    self._log(15, message, args, **kwargs)

            logging.Logger.start = start

            # Avoid adding multiple handlers if logger is reused
            if not logger.handlers:
                # Setup formatter
                formatter = logging.Formatter(
                    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )

                # File handler
                log_filename = os.path.join(
                    log_dir, f"log_{datetime.now().strftime('%Y%m%d')}.log"
                )
                file_handler = logging.FileHandler(log_filename)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

                # Console handler
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

            ApplicationLogger._logger = logger

        return ApplicationLogger._logger
