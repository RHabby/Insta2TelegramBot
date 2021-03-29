import logging


logging.basicConfig(filename="./bot_logger.log",
                    format="%(asctime)s: %(name)s: %(levelname)s: %(funcName)s: [LINE: %(lineno)d]: %(message)s",
                    level=logging.INFO)
