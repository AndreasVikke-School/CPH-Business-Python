import sys
import logging
import getopt
import Ex1
from pprint import pprint


log_fmt = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_fmt)


def usage():
    return 'Usage : cli-Ex1.py csv_path --file file_name'


def run(arguments):
    try:
        opts, args = getopt.getopt(arguments, "ho:v", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for option, argument in opts:
        if(option in ("-h", "--help")):
            print(usage())
            sys.exit()

    if len(args) > 1:
        result = ""
        for s in Ex1.read_csv(args[0]):
            result += s[0]

        Ex1.write_list_to_file(args[1].split('=')[1], result)
        sys.exit()
    else:
        pprint(Ex1.read_csv(args[0]))
        sys.exit()

if __name__ == '__main__':
    # Call me from the CLI for example with:
    # python your_script.py arg_1 [arg_2 ...]
    run(sys.argv[1:])
