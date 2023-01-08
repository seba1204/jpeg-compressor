from src.arguments import parse_args, check_safe_ouput
from src.logger import set_logger


def main():
    """Main function"""
    # parse the console arguments
    args = parse_args()
    logger = set_logger(args)

    # check ouput overwriting
    check_safe_ouput(args, logger)

    # run the test suite
    if args.test:
        # TODO: create and run the test suite
        return


if __name__ == "__main__":
    main()
