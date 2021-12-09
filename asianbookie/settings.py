import logging
import os
from pathlib import Path

ASIAN_BOOKIE_URL = "https://tipsters.asianbookie.com"
ASIAN_BOOKIE_TOP_TIPSTERS_URL = "https://tipsters.asianbookie.com/index.cfm?top20=1"

APP_USER_DIR = Path.home() / ".asianbookie"

DATA_DIR = APP_USER_DIR / "data"
LOG_DIR = APP_USER_DIR / "logs"

PICKLE_FILE = APP_USER_DIR / ".asianbookie_cache"
LOG_FILE = LOG_DIR / "asianbookie.log"


def setup():
    setup_data_directory()
    setup_logger()


def setup_logger():
    format_str = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    log_file = LOG_FILE

    logging.basicConfig(
        level=logging.DEBUG,
        format=format_str,
        datefmt="%m-%d %H:%M",
        filename=log_file,
        filemode="a+",
    )
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter(format_str)
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger("").addHandler(console)


def setup_data_directory():
    os.makedirs(APP_USER_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    PICKLE_FILE.touch(exist_ok=True)
