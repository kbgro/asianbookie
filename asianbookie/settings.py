import logging

ASIAN_BOOKIE_URL = "https://tipsters.asianbookie.com"
ASIAN_BOOKIE_TOP_TIPSTERS_URL = "https://tipsters.asianbookie.com/index.cfm?top20=1"


def setup_logger():
    format_str = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    logging.basicConfig(
        level=logging.DEBUG,
        format=format_str,
        datefmt="%m-%d %H:%M",
        filename="asianbookie.log",
        filemode="w",
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
