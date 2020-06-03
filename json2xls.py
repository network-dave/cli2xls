#!/usr/bin/env python3

'''

Name:           json2xls.py
Description:    Read JSON data and write a flattened table in XLS or CSV format
Author:         David Paneels

Usage:          see json2xls.py --help

'''

import argparse
import sys
import os
import json
import csv
import re
import logging

from openpyxl import Workbook
from openpyxl import load_workbook

import cli2json


# Global options
DELIMITER = ";"
DEFAULT_OS = "nxos"
DEFAULT_PARSER = "default"


def parse_json_to_table(json_data, device_os, parser):
    '''
    Make a flattened table out of JSON data according to a specific parser
    '''
    # Put the dashes back into the parser name to load the file (yes, I know...)
    parser = parser.replace(" ", "-")

    # Import the JSON parser module from the jsonparsers/os subdirectory
    path = os.path.join(".", "jsonparsers", device_os)
    logging.debug(f"[+] Loading JSON parser module {os.path.join(path, parser)}")
    sys.path.append(os.path.abspath(path))

    # If the specified module does not exist in jsonparsers/ import the default parser
    if not os.path.exists(os.path.join(path, parser+".py")):
        logging.debug("[+] No file found, loading default JSON parser module")
        parser = DEFAULT_PARSER

    try:
        jsonparser = __import__(parser)
    except Exception as e:
        logging.critical(f"[!] Error while loading JSON parser module (exit code 1)")
        logging.critical(f"[!] {str(e)}")
        sys.exit(1)

    # Make flattened table out of JSON data
    table = jsonparser.parse(json_data)

    return table

def add_table_to_workbook(table, filename, sheetname="default"):
    '''
    Add table data to a new worksheet in an Excel file
    '''
    # If XLS file exists, insert the table in a new worksheet else create a new workbook file
    if os.path.exists(filename):
        wb = load_workbook(filename)
        logging.debug(f"[+] Workbook {filename} already exists, adding new worksheet to it")
        if sheetname in wb.sheetnames:
            ws = wb.create_sheet(sheetname + " NEW")
        else:
            ws = wb.create_sheet(sheetname)
    else:
        logging.debug(f"[+] Creating new Excel workbook {filename}")
        wb = Workbook()
        ws = wb.active
        ws.title = sheetname

    for row in table:
        ws.append(list(row))
    
    wb.save(filename = filename)


def main():
    '''
    Main program
    '''
    # Parse command line arguments
    argparser = argparse.ArgumentParser(
        description="Read JSON data and write an XLS/CSV file"
        )
    argparser.add_argument(
        "--infile",
        metavar="inputfile.json",
        required=True,
        type=argparse.FileType("r"),
        help="JSON file (use '-' to read from stdin)",
        )
    argparser.add_argument(
        "--outfile",
        metavar="FILENAME",
        help="save output to Excel or CSV file (supported formats: .xls, .xlsx, .csv)"
        )
    argparser.add_argument(
        "--os",
        default=DEFAULT_OS,
        help=f"network OS which originated the output (default={DEFAULT_OS})"
        )
    argparser.add_argument(
        "--parser",
        #default=DEFAULT_PARSER,    # if we do this we can't overwrite the default parser later on
        help="JSON parser (default=infered from filename, fallback to jsonparser/os/default.py)"
        )
    argparser.add_argument(
        "--verbose",
        action="store_true",
        help="print additional information to stderr"
        )
    args = argparser.parse_args()

    # Configure logging
    if args.verbose:
        logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    else:
        logging.basicConfig(format="%(message)s", level=logging.INFO)

    # Load and deserialize JSON data from filehandler (it has already been opened by argparse)
    with args.infile as f:
        infilename = f.name
        logging.debug(f"[+] Loading JSON data from {infilename}")
        json_data = json.loads(f.read())

    # If no data is present we'll just exit with error code 1
    if not json_data:
        sys.exit(1)

    # Select JSON parser or infer from filename
    if args.parser:
        parser = args.parser
    else:
        parser = cli2json.get_parser_from_filename(infilename)

    logging.debug(f"[+] Using parser '{parser}'")
    table = parse_json_to_table(json_data, args.os, parser)

    # Export the data according to the file type specified
    if args.outfile:
        if ".csv" in args.outfile:
            with open(args.outfile, "w") as f:
                c = csv.writer(f, delimiter=DELIMITER)
                for row in table:
                    c.writerow(row)
        elif ".xls" in args.outfile:        # Also works for .xlsx
            add_table_to_workbook(table, args.outfile, sheetname=parser)
        logging.info(f"[+] Done writing data to {args.outfile}")
    else:
        # If no output file is specified just print raw text to stdout
        for row in table:
            print("\t".join(str(s) for s in row))

if __name__ == "__main__":
    '''
    main()
    '''
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
    except json.decoder.JSONDecodeError:
        logging.warning("[!] An error occured while decoding the JSON data (exit code 1)")
        sys.exit(1)
    except Exception as e:
        logging.warning("[!] An error occured during the operation (exit code 1)")
        logging.warning("[!] " + str(e))
        #raise e
        sys.exit(1)
    