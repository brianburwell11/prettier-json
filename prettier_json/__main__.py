import argparse
import json
import pathlib
import sys

from prettier_json.prettier_json import (
    DEFAULT_INDENT_SIZE,
    DEFAULT_MAXLINELENGTH,
    __version__,
    prettyjson,
)

parser = argparse.ArgumentParser(
    prog="prettier_json", description="Generate prettier and more compact JSON files."
)
parser.add_argument(
    "-v", "--version", action="version", version=f"%(prog)s {__version__}"
)
parser.add_argument(
    "json_files",
    metavar="JSON_PATH",
    type=pathlib.Path,
    nargs="+",
    help="path to a .json file",
)
parser.add_argument(
    "-i",
    "--indent",
    metavar="INDENT_SIZE",
    type=int,
    nargs="?",
    default=DEFAULT_INDENT_SIZE,
    help=f"number of spaces to use as an indent. Default={DEFAULT_INDENT_SIZE}",
)
parser.add_argument(
    "-l",
    "--line-length",
    metavar="MAX_LENGTH",
    type=int,
    nargs="?",
    default=DEFAULT_MAXLINELENGTH,
    help=f"how many characters to allow on a single line before wrapping to a newline. Default={DEFAULT_MAXLINELENGTH}",
)

args = parser.parse_args()

for json_file in args.json_files:
    try:
        with open(json_file, "r") as f:
            json_contents = json.load(f)
    except FileNotFoundError:
        sys.exit(f"ERROR: {json_file} doesn't exist.")
    except IsADirectoryError:
        sys.exit(
            f"ERROR: Paths must be to a valid JSON file. {json_file} is a directory."
        )
    except json.decoder.JSONDecodeError:
        sys.exit(f"ERROR: {json_file} is not valid JSON")

    json_contents = prettyjson(
        json_contents, indent=args.indent, maxlinelength=args.line_length
    )
    with open(json_file, "w") as f:
        f.write(json_contents)
