import logging
import os
import sys
from enum import IntEnum

HANDLERS = [logging.StreamHandler(sys.stdout)]
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", logging.DEBUG)


class EnvType(IntEnum):
    PROD = 1
    NONPROD = 0
    DEV = -1


class CustomFormatter(logging.Formatter):
    """Custom Formatter does these 2 things:
    1. Overrides 'funcName' with the value of 'func_name_override', if it exists.
    2. Overrides 'filename' with the value of 'file_name_override', if it exists.
    """

    def format(self, record):
        if hasattr(record, 'func_name_override'):
            record.funcName = record.func_name_override
        if hasattr(record, 'file_name_override'):
            record.filename = record.file_name_override
        return super(CustomFormatter, self).format(record)


def get_logger(handlers=HANDLERS):
    """Creates a Log File and returns Logger object"""

    formatter = CustomFormatter(
        '%(asctime)s - %(levelname)-9s -'
        ' %(filename)s - %(funcName)s - %(message)s'
    )

    for handler in handlers:
        handler.setFormatter(formatter)

    logging.basicConfig(
        level=LOGGING_LEVEL,
        handlers=handlers,
    )

    # Return logger object
    return logging.getLogger(__name__)
