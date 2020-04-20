import os
import sys
import traceback

from utils import create_cli


def main():
    omniscript_path = os.path.dirname(__file__)
    supported_benchmarks = ["ny_taxi", "santander", "census", "plasticc", "mortgage"]

    os.environ["PYTHONIOENCODING"] = "UTF-8"
    os.environ["PYTHONUNBUFFERED"] = "1"

    interface = create_cli(omniscript_path, supported_benchmarks)

    try:
        args = interface.parse_args()
        args.func(args)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)


if __name__ == "__main__":
    main()
