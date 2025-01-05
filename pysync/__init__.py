import argparse
from pathlib import Path

import pysync.logging as logging
from fs_sync import sync

PROGRAM_NAME = "pysync"


def command_entry_point():
    try:
        main()
    except KeyboardInterrupt:
        print("Program was interrupted by user")


def main():
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME,
                                     description="A simple python script (cli and package) for syncing files between directories",
                                     allow_abbrev=True, add_help=True, exit_on_error=True)

    parser.add_argument("source", metavar="SRC", help="The source path from which to sync")
    parser.add_argument("destinations", metavar="DEST...", nargs=argparse.REMAINDER,
                        help="The paths to which to sync to")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Disables checks for whether modification time and file size are different and always copies all files")
    parser.add_argument("-d", "--delete", action="store_true",
                        help="Allows the program to delete files if they don't exist in the source")
    parser.add_argument("-nc", "--no-color", action="store_true",
                        help="Disables the use of color in the console output (using ANSI escape codes)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Output no information messages to the console")
    parser.add_argument("-ct", "--create-toplevel", action="store_true",
                        help="Create the destination path if it does not exist. Without this option that destination is simply skipped.")
    parser.add_argument("--version", action="store_true", help="Show the current version of the program")

    args = parser.parse_args()
    use_color = not args.no_color

    if args.version:
        logging.log(PROGRAM_NAME, "version", version.program_version, use_color=use_color)
        return

    source = Path(args.source)

    if not source.exists():
        logging.log(f"The source path {source} does not exist", use_color=use_color)
        return

    destinations = [Path(d) for d in args.destinations]

    for d in destinations:
        if d.exists(): continue
        logging.log(f"The destination path {d} does not exist", use_color=use_color)

        if args.create_toplevel:
            d.touch()

    for d in destinations:
