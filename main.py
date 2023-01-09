from lib.compressor import compress
from src.arguments import check_safe_ouput, log_args, parse_args
from src.logger import set_logger


def main():
    """Main function"""
    # parse the console arguments
    try:
        args = parse_args()
        logger = set_logger(args)
    except ValueError as e:
        print(e)
        return

    # check ouput overwriting
    if check_safe_ouput(args, logger):
        return

    logger.debug(log_args(args))

    # run the test suite
    if args.test:
        # TODO: create and run the test suite
        return

    # for each input file, compress it
    for i in range(len(args.input)):
        compress(args.input[i], args.output[i], args, logger)


if __name__ == "__main__":
    main()
