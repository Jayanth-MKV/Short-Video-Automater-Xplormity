import logging

class MultiLogger:
    def __init__(self, name, file_path, log_to_console=True):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')

        # File Handler
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console Handler
        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        

    def get_logger(self):
        return self.logger


