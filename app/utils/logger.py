from loguru import logger
import sys


def setup_logger():
    logger.remove()

    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level}</level> | "
               "<cyan>{message}</cyan>"
    )

    return logger


log = setup_logger()
