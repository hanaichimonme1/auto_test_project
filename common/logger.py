import  logging
def get_logger():
    logger=logging.getLogger("api_test")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        console_handler=logging.StreamHandler()
        formatter=logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        file_handler = logging.FileHandler("test.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger