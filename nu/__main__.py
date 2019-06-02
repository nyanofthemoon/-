import asyncio
import os
import sys

if sys.version_info < (3, 6, 6):
    sys.stderr.write("Python 3.6.6 or later required to run this script" + os.linesep)
    exit(1)

import argparse
import logging
from .modules.runner import main_function

parser = argparse.ArgumentParser()
parser.add_argument("-v", help="Enable verbose mode", required=False, nargs='?', const=1, default=None)
parser.add_argument("-vv", help="Enable very verbose mode", required=False, nargs='?', const=1, default=None)

if __name__ == "__main__":
    args = parser.parse_args()

    logger = logging.getLogger()
    if (args.vv != None):
        logger.setLevel(logging.DEBUG)
    elif (args.v != None):
        logger.setLevel(logging.INFO)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_function())
    loop.close()
