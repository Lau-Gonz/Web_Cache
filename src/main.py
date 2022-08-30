#!/usr/bin/env python3.10
import sys
from server import main as server
from client import main as client


def main(argc: int, argv: list[str]) -> None:
    if argc > 1:
        match argv[1].lower():
            case "server":
                return server()
            case _:
                assert ValueError("argv not supported")


if __name__ == "__main__":
    argv = sys.argv
    main(len(argv), argv)
    server()
    client()

