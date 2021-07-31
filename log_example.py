# %%


import logging
import sys

from logger import *


# %%

fh = logging.FileHandler(filename=f"{__file__}.log")
ch = logging.StreamHandler(sys.stdout)
logs = get_logger(handlers=[fh, ch])


@log_decorator(handlers=[fh, ch])
def sum(a=1, b=2):
    logs.debug("test")
    return a + b


sum(5, 6)
# %%
