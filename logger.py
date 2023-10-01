import loguru

def setup_logger():
    logger = loguru.logger
    logger.add('data.txt', format="{time} {message}", level='INFO')
    return logger
