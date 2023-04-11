import argparse
import logging
import os
import sys

LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
logging.basicConfig(format="%(asctime)s %(message)s", level=LOGLEVEL)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-delay-seconds", default=5, type=int)
    parser.add_argument("--error-delay-seconds", default=3, type=int)
    args = parser.parse_args()

    data = sys.stdin.readlines()
    print(data)


if __name__ == "__main__":
    main()
