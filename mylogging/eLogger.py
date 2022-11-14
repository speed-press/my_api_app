"Endpoint logging decorator"
import functools


def elog(e_name, _func=None, *, loggers: dict):
    """ Logging decorator. Modified slightly to better fit this 
    https://ankitbko.github.io/blog/2021/04/logging-in-python/
    """
    def decorator_log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = loggers['endpoint']
            loggerE = loggers['root']
            loggerD = loggers['data']
            logger.debug( f'Endpoint {e_name} initiated')
            try:
                result = func(*args, **kwargs)
                logger.debug('Endpoint successfully retrieved data')
                loggerD.debug(f'Endpoint retrieved data: result = {result}')
                return result
            except Exception as e:
                name = func.__name__
                loggerE.exception(
                    f"Exception raised in {name} on endpoint {e_name} exception: {str(e)}")
                raise e
        return wrapper
    if _func is None:
        return decorator_log
    else:
        return decorator_log(_func)

