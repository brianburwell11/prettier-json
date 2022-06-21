import argparse
import json
import pathlib
import sys

from prettier_json.prettier_json import __version__, prettyjson

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
    default=2,
    help="number of spaces to use as an indent",
)
parser.add_argument(
    "-l",
    "--line-length",
    metavar="MAX_LENGTH",
    type=int,
    nargs="?",
    default=80,
    help="how many characters to allow on a single line before wrapping to a newline",
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
