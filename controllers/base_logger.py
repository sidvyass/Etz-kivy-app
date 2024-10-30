import sys
import loguru
import logging


def getlogger(name: str = "DefaultName", level="DEBUG") -> loguru.logger:  # type: ignore
    """
    Initialize and return a logger instance with the specified name and level.
    """

    logobj = loguru.logger.bind(name=name)

    logobj.remove()

    logger_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "{extra[name]} | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    logobj.add(
        sys.stderr,
        level=level,
        format=logger_format,
        colorize=True,
        serialize=False,
    )

    return logobj
