import argparse
import os
from src.constants import PROG_VERSION, DEFAULT_RATIO
import logging


class Arguments:
    def __init__(self):
        self.debug: bool = False
        self.logfile = None
        self.version: str = PROG_VERSION
        self.ratio: float = 0.5
        self.input: list[str] = []
        self.dangerous_input: list[str] = []
        self.output = None
        self.force: bool = False
        self.quiet: bool = False
        self.test: bool = False
        self.compare: bool = False


def define_args() -> argparse.ArgumentParser:
    # parse the console arguments
    parser = argparse.ArgumentParser(description="JPEG compression")

    parser.add_argument("-d", "--debug",
                        action="store_true",
                        help="enable debug mode")

    parser.add_argument("-v", "--version",
                        action="version",
                        version="%(prog)s " + PROG_VERSION,
                        help="show program's version number and exit")

    parser.add_argument("-r", "--ratio",
                        type=float,
                        default=DEFAULT_RATIO,
                        help="set the ratio of the JPEG compression [0, 1]")

    parser.add_argument("-i", "--input",
                        type=str,
                        help="path to the input image, can be a file or a directory, must be set")

    parser.add_argument("-o", "--output",
                        type=str,
                        help="path to the output image, can be a file or a directory, if not set, the output will be the same as the input image")

    parser.add_argument("-q", "--quiet",
                        action="store_true",
                        default=False,
                        help="disable the console output")

    parser.add_argument("-f", "--force",
                        action="store_true",
                        default=False,
                        help="force the overwrite of the output file (if it exists)")

    parser.add_argument("-t", "--test",
                        action="store_true",
                        default=False,
                        help="run the test suite")

    parser.add_argument("-c", "--compare",
                        action="store_true",
                        default=False,
                        help="compare quality of the output image with the input image")

    return parser


def get_in_out_files(args: argparse.Namespace) -> tuple[list[str], list[str]]:
    safe_input = []
    safe_output = []
    # check if there is an input file
    if not args.input:
        raise ValueError(
            "The input file must be set. Use -h or --help for more information.")

    # check if the input file exists
    if not os.path.isfile(args.input):
        raise ValueError("The input file does not exist.")

    assert (args.input)

    # check if the input is a file or a directory.
    # if it is a directory, then loop through all the files in the directory and save path into a list
    # else create a list with one element
    if os.path.isfile(args.input):
        safe_input = [args.input]
    elif os.path.isdir(args.input):
        paths = os.listdir(args.input)
        # for each path in the directory, check if it is an image (jpg, jpeg, png, bmp, tiff, gif, webp, CR2)
        for path in paths:
            if os.path.isfile(path):
                if path.endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif", ".webp", ".CR2")):
                    safe_input.append(path)
    else:
        raise ValueError(
            "The input file is not a file or a directory ¯\_(ツ)_/¯")

    # check if there is an output
    if not args.output:
        # if not, the output is the same as the input
        safe_output = safe_input
    else:
        # if there is an output, check if it is the same as the input
        # if input is a directory, the output must be a directory too
        # if input is a file, the output can be a file or a directory
        if os.path.isdir(args.input):
            if os.path.isdir(args.output):
                # for each input file, create a path to the output file
                for input_file in safe_input:
                    # get the input file name
                    input_file_name = os.path.basename(input_file)
                    safe_output.append(
                        os.path.join(args.output, input_file_name))
            else:
                raise ValueError(
                    "The input is a directory, the output must be a directory too. Else, all output except the last one will be overwritten.")
        else:
            if os.path.isdir(args.output):
                input_file_name = os.path.basename(safe_input[0])
                safe_output = [os.path.join(args.output, input_file_name)]
            else:
                safe_output = [args.output]

    assert (len(safe_input) == len(safe_output))
    assert (len(safe_input) > 0)

    return [safe_input, safe_output]


def get_ratio(args: argparse.Namespace) -> float:
    # check if there is a ratio
    ratio = 0
    if not args.ratio:
        ratio = DEFAULT_RATIO
    else:
        ratio = args.ratio
        if ratio < 0 or ratio > 1:
            raise ValueError(
                "The ratio (" + str(ratio) + ") must be between 0 and 1. Use -h or --help for more information.")
        else:
            return ratio


def check_safe_ouput(safe_args: Arguments, logger: logging.Logger) -> None:
    # check if the output file exists
    unsafe_output = []
    for output_file in safe_args.output:
        if os.path.isfile(output_file):
            unsafe_output.append(output_file)

    if len(unsafe_output) > 0:
        if len(unsafe_output) > 1:
            message = unsafe_output.join(", ") + " already exist."
        else:
            message = unsafe_output[0] + " already exists."
        if safe_args.force:
            logger.warning(message + " Overwriting...")
        else:
            raise ValueError(message + " Use -f or --force to overwrite it.")


def check_args(args: argparse.Namespace) -> Arguments:
    safe_args = Arguments()

    [input_files, output_files] = get_in_out_files(args)

    safe_args.input = input_files
    safe_args.output = output_files

    safe_args.force = args.force
    safe_args.quiet = args.quiet
    safe_args.debug = args.debug
    safe_args.test = args.test
    safe_args.compare = args.compare

    safe_args.ratio = get_ratio(args)

    return safe_args


def parse_args() -> Arguments:
    parser = define_args()
    args = parser.parse_args()

    # check args
    return check_args(args)
