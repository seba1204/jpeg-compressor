import argparse
import logging
import os
from os.path import dirname, isdir, isfile
from os.path import join as join_path

import src.error_messages as em
from src.constants import DEFAULT_RATIO, PROG_VERSION
from src.helpers import fn_without_ext, is_image, join, replace_extension


class Arguments:
    def __init__(self):
        self.debug: bool = False
        self.logfile = None
        self.version: str = PROG_VERSION
        self.ratio: float = 0.5
        self.input: list[str] = []
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
        raise ValueError(em.INPUT_FILE_MISSING)
    assert (args.input)

    # check if the input is a file or a directory.
    # if it is a directory, then loop through all the files in the directory and save path into a list
    # else create a list with one element
    if isfile(args.input):
        if is_image(args.input):
            safe_input = [args.input]
        else:
            raise ValueError(em.NOT_RECOCGNISED_IMAGE_FORMAT)
    elif isdir(args.input):
        paths = os.listdir(args.input)
        for img_path in paths:
            full_path = join_path(args.input, img_path)
            if isfile(full_path):
                if is_image(full_path):
                    safe_input.append(full_path)
        if not safe_input:
            raise ValueError(em.NO_IMG_RECOGNIZED_IN_DIRECTORY)
    else:
        raise ValueError(em.INPUT_FILE_NOT_A_FILE_OR_A_DIRECTORY)

    # SET OUTPUT FILES ---------------------------------------------------------
    if not args.output:
        safe_output = [replace_extension(file, ".jpg") for file in safe_input]
    else:
        # if there is an output, check if it is the same as the input
        # if input is a directory, the output must be a directory too
        # if input is a file, the output can be a file or a directory
        if isdir(args.input):
            if isfile(args.output):
                raise ValueError(em.INPUT_IS_DIRECTORY_BUT_OUTPUT_IS_FILE)
            else:
                # check if the output directory exists
                if not isdir(args.output):
                    os.makedirs(args.output)
                # for each input file, create a path to the output file
                for input_file in safe_input:
                    # get the input file name
                    input_fn_without_ext = fn_without_ext(input_file)
                    # create the output file path
                    safe_output.append(
                        join_path(args.output, input_fn_without_ext + ".jpg"))

        else:
            if isdir(args.output):
                input_fn_without_ext = fn_without_ext(args.input)
                input_file_name = input_fn_without_ext + ".jpg"
                safe_output = [join_path(args.output, input_file_name)]
            else:
                # check if the output file ends with .jpg
                if not args.output.endswith(".jpg"):
                    raise ValueError(em.OUTPUT_FILE_MUST_END_WITH_JPG)
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
            raise ValueError(em.RATIO_OUT_OF_BOUNDS, ratio)
        else:
            return ratio


def check_safe_ouput(safe_args: Arguments, logger: logging.Logger) -> int:
    # check if the output file exists
    unsafe_output = []
    for output_file in safe_args.output:
        if isfile(output_file):
            # if it ends with .jpg or .jpeg, then add it to the list
            if output_file.endswith((".jpg", ".jpeg")):
                unsafe_output.append(output_file)

    if len(unsafe_output) > 0:
        if len(unsafe_output) > 1:
            message = join(unsafe_output, ", ") + em.ALREADY_EXIST
        else:
            message = unsafe_output[0] + em.ALREADY_EXISTS

        if safe_args.force:
            logger.warning(message + em.OVERWRITING)
            return 0
        else:
            logger.error(
                message + em.NO_OUTPUT_BUT_OVERWRITE_NOT_SET)
            return 1
    else:
        return 0


def log_args(args: Arguments) -> str:
    inputs = join(args.input, "\n----")
    outputs = join(args.output, "\n----")
    ratio = str(args.ratio)
    force = str(args.force)
    quiet = str(args.quiet)
    debug = str(args.debug)
    test = str(args.test)
    compare = str(args.compare)

    return "\n--Input: " + inputs + "\n" + \
        "--Output: " + outputs + "\n" + \
        "--Ratio: " + ratio + "\n" + \
        "--Force: " + force + "\n" + \
        "--Quiet: " + quiet + "\n" + \
        "--Debug: " + debug + "\n" + \
        "--Test: " + test + "\n" + \
        "--Compare: " + compare + "\n"


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
