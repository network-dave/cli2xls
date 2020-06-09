#!/usr/bin/env python

'''

Name:           cli2xls.py 
Description:    Use cli2json.py and json2xls.py to parse and export raw CLI output directly to Excel spreadsheets
Author:         David Paneels

Usage:          see cli2xls.py --help
    
'''

import argparse
import sys
import os
import logging

import cli2json
import json2xls

# DEFAULT OPTIONS
DEFAULT_OS = "nxos"


def main():
    '''
    Main program
    '''
    # Parse command line argument
    argparser = argparse.ArgumentParser(
        description="Read network device CLI output and parse it to an Excel spreadsheet"
        )
    argparser.add_argument(
        "--infile",
        metavar="inputfile.txt",
        required=True,
        type=argparse.FileType("r"), 
        help="text file containing show commands output (use '-' for stdin)"
        )
    argparser.add_argument(
        "--outfile",
        metavar="outputfile.xlsx",
        #required=True,
        help="output to XLS file (default=use device_name.xlsx as filename)"
        )        
    argparser.add_argument(
        "--os",
        default=DEFAULT_OS,
        help=f"network OS which originated the output (default={DEFAULT_OS})"
        )
    argparser.add_argument(
        "--parser",
        #default=DEFAULT_PARSER,    # if we do this we can't overwrite the default parser later on
        help="Parser/template to use (default=infered from filename)"
        )
    argparser.add_argument(
        "--verbose",
        action="store_true",
        help="print additional information to stderr"
        )
    args = argparser.parse_args()

    # Configure logging
    if args.verbose:
        logging.basicConfig(format="%(message)s", level=logging.INFO)
    else:
        logging.basicConfig(format="%(message)s", level=logging.WARNING)

    # Load text data from file handler (it has already been opened by argparse)
    with args.infile as f:
        infilename = f.name
        cli_output = f.read()

    # If no parser/template is specified we'll extract it from the filename or fallback to the default parser
    device_name = cli2json.get_device_name_from_filename(infilename)
        
    # Select parser/template or infer from filename
    if args.parser:
        parser = args.parser
    else:
        parser = cli2json.get_parser_from_filename(infilename)

    # Parse CLI to JSON data
    json_data = cli2json.parse_cli_to_json(device_name, args.os, parser, cli_output)

    # Create flattened table out of JSON data
    table = json2xls.parse_json_to_table(json_data)

    if not args.outfile:
        args.outfile = device_name + ".xlsx"
    
    # Open workbook and write table to worksheet
    json2xls.add_table_to_workbook(table, args.outfile, parser)
    

if __name__ == "__main__":
    '''
    main()
    '''
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
    except Exception as e:
        logging.critical(f"[!] An error occured during the operation ({str(e)})")
        #raise e
        sys.exit(1)
