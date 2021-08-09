import functools
import os
import sys
import traceback

from .custom_log import get_logger, EnvType

ENVTYPE = EnvType[os.getenv("ENV_TYPE", "NONPROD")]
LINEFEED = "\\n"
CARRIAGERETURN = "\\r"


def log_decorator(handlers, _func=None, lf=LINEFEED, cr=CARRIAGERETURN):
    def log_decorator_info(func):
        @functools.wraps(func)
        def log_decorator_wrapper(*args, **kwargs):
            # Build logger object
            logs = get_logger(handlers=handlers)
            args_passed_in_function = [repr(a) for a in args]
            kwargs_passed_in_function = [
                f"{k}={v!r}" for k, v in kwargs.items()
            ]
            formatted_arguments = ", ".join(
                args_passed_in_function + kwargs_passed_in_function
            )
            extra_args = {
                'func_name_override': func.__name__,
                'file_name_override': os.path.basename(
                    func.__globals__['__file__']
                ),
            }
            logs.info(
                f"Arguments: {formatted_arguments} - Begin function",
                extra=extra_args,
            )
            try:
                value = func(*args, **kwargs)
                logs.info(
                    f"Returned: - End function {value!r}",
                    extra=extra_args,
                )
            except:
                trace_msg = (
                    str(sys.exc_info()[1]).replace('\n', lf).replace('\r', cr)
                )
                logs.error(
                    f"Exception: {trace_msg}",
                    extra=extra_args,
                )
                if ENVTYPE < int(EnvType.PROD):
                    err = (
                        traceback.format_exc()
                        .replace('\n', lf)
                        .replace('\r', cr)
                    )
                    logs.error(err, extra=extra_args)
                raise
            # Return function value
            return value

        # Return the pointer to the function
        return log_decorator_wrapper

    # Decorator was called with arguments, so return a decorator function
    # that can read and return a function
    if _func is None:
        return log_decorator_info
    # Decorator was called without arguments, so apply the decorator
    # to the function immediately
    else:
        return log_decorator_info(_func)
