import sys
import os

import argparse

from . import freeze_to_string

# Based on what pip does, but try to be brief and not hardcode our name
def get_prog() -> str:
    package = __loader__.name.split(".")[0]
    try:
        prog = os.path.basename(sys.argv[0])
        if prog in ("__main__.py", "-c"):
            # go back to orig_argv[0] to get what the user used
            return f"{sys.orig_argv[0]} -m {package}"
        else:
            return prog
    except (AttributeError, TypeError, IndexError):
        pass
    return package

def main() -> int:
    parser = argparse.ArgumentParser(
        prog = get_prog(),
        description  = 'Create a single-file version of an HTML file',
    )
    parser.add_argument('url')
    parser.add_argument(
        '-T', '--timeout',
        type=float,
        default=900.0,
        help='default connect and read timeout in seconds'
    )
    parser.add_argument(
        '--connect-timeout',
        type=float,
        help='default connect timeout in seconds (will override --timeout)'
    )
    parser.add_argument(
        '--read-timeout',
        type=float,
        help='default read timeout in seconds (will override --timeout)'
    )

    args = parser.parse_args()

    timeout = args.timeout
    if (args.connect_timeout or args.read_timeout):
        timeout = (args.connect_timeout or timeout, args.read_timeout or timeout)

    print(freeze_to_string(args.url, timeout=timeout))

    return 0

if __name__ == '__main__':
    sys.exit(main())
