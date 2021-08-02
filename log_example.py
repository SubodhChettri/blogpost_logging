# %%


import logging
import sys


from logger import get_logger, log_decorator


# %%


fh = logging.FileHandler(filename=f"{__file__}.log")
ch = logging.StreamHandler(sys.stdout)
handlers = [
    fh,
    # ch
]
logs = get_logger(handlers=handlers)


@log_decorator(handlers=handlers)
def sum(first_number=1, second_number=2):
    logs.info(f"Adding 2 numbers {first_number} and {second_number}")
    return first_number + second_number


def main():
    tuples = [(5, 6), ('a', 'b'), (6, 'c'), ('d', 10)]
    counter = 1
    for a, b in tuples:
        try:
            logs.info(f"Call # {counter}")
            sum(a, b)
            counter += 1
        except Exception:
            logs.error('check input data type')


# %%
if __name__ == "__main__":
    main()
