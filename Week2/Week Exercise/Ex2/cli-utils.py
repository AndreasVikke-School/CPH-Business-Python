import sys
import logging
import utils

log_fmt = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_fmt)

def usage():
     return 'Usage: python cli-utils.py md_file'

def run(arguments):
    l = []
    for argument in arguments:
        l.append(argument)
    utils.print_headers_of_md(l)


if __name__ == '__main__':
    # Call me from the CLI for example with:
    # python your_script.py arg_1 [arg_2 ...]
    run(sys.argv[1:])