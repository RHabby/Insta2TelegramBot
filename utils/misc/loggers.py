import inspect
import logging


logging.basicConfig(filename="./bot_logger.log",
                    format="%(asctime)s: %(name)s: %(levelname)s: %(funcName)s: [LINE: %(lineno)d]: %(message)s",
                    level=logging.INFO)


def log_event(*args, level: str = "info"):
    frame = inspect.currentframe()
    outer_frame = inspect.getouterframes(frame)[1].function

    log_string = (": ").join([str(arg) for arg in args])

    if level == "error":
        logging.error(f'[FUNC: {outer_frame}]: {log_string}')
    else:
        logging.info(f'[FUNC: {outer_frame}]: {log_string}')
