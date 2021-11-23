import logging
import os
from pathlib import Path

ASIAN_BOOKIE_URL = "https://tipsters.asianbookie.com"
ASIAN_BOOKIE_TOP_TIPSTERS_URL = "https://tipsters.asianbookie.com/index.cfm?top20=1"

DATA_DIR = Path(__file__).resolve(True).parent.parent / "data"
LOG_DIR = Path(__file__).resolve(True).parent.parent / "logs"


def setup():
    setup_data_directory()
    setup_logger()


def setup_logger():
    format_str = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    log_file = LOG_DIR / "asianbookie.log"

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
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
