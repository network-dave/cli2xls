#!/usr/bin/env python

'''

Name:           cli2singlexls.py 
Description:    Parse multiple text files to a single Excel workbook
Author:         David Paneels

Usage:          see cli2singlexls.py --help
    
'''

import argparse
import sys
import os
import logging
import glob

import cli2json
import json2xls

# DEFAULT OPTIONS
DEFAULT_OS = "ios"


def main():
    '''
    Main program
    '''
    # Parse command line argument
    argparser = argparse.ArgumentParser(
        description="Read network device CLI output and parse it to an Excel spreadsheet"
        )
    argparser.add_argument(
        "-i",
        "--infile",
        metavar="/path/to/*.txt",
        required=True,
        help="text files containg CLI output (use quotes around it!)"
        )
    argparser.add_argument(
        "-o",
        "--outfile",
        metavar="outputfile.xlsx",
        required=True,
        help="output filename"
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

    # Global results tables
    result = []
    i = 0

    for infile in glob.glob(args.infile):
        # Load text data from file handler (it has already been opened by argparse)
        with open(infile) as f:
            cli_output = f.read()

        # If no parser/template is specified we'll extract it from the filename or fallback to the default parser
        device_name = cli2json.get_device_name_from_filename(infile)
            
        # Select parser/template or infer from filename
        if args.parser:
            parser = args.parser
        else:
            parser = cli2json.get_parser_from_filename(infile)

        # Parse CLI to JSON data
        json_data = cli2json.parse_cli_to_json(device_name, args.os, parser, cli_output)

        # Create flattened table out of JSON data, only add the header once
        try:
            if i == 0:
                table = json2xls.parse_json_to_table(json_data)
                # Add the device_name as the first column of the table
                table[0] = [ "DEVICE" ] + table[0]
                table[1] = [ device_name ] + table[1]
            else:
                table = json2xls.parse_json_to_table(json_data, add_header=False)
                table[0] = [ device_name ] + table[0]
        except:
            logging.warn(f"[!] Error while parsing file {infile}")

        # Append the entry to the result table
        result += table
        i += 1

    # Open workbook and write table to worksheet
    json2xls.add_table_to_workbook(result, args.outfile, parser)
    

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
        raise e
        sys.exit(1)
