import sys
from urllib.parse import urlparse
import logging
import Modules.webget as webget


log_fmt = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_fmt)


def check_args(arguments):
    if len(arguments) == 0:
        return False
    for arg in arguments:
        if not webget.check_url(arg):
            return False
    return True

def usage():
    return 'Usage : cli-webget.py url [url]...'

def run(arguments):
    if check_args(arguments):
        for argument in arguments:
            f = webget.download(argument)
            logging.info('Downloading file to {}'.format(f))
    else:
        print(usage())


if __name__ == '__main__':
    # Call me from the CLI for example with:
    # python your_script.py arg_1 [arg_2 ...]
    run(sys.argv[1:])