#!/usr/bin/env python

'''

Name:           cli2json.py 
Description:    Read network device CLI command output from text file or stdin and output JSON structured data
Author:         David Paneels

Usage:          see cli2json.py --help
    

Automatic parser selection:

    The Genie parser to use will be infered from the filename:
        MyDevice_show-interfaces-status.txt -> "show interfaces status"
        MyDevice_show-vlan_12345.txt -> "show vlan"

    The device name MUST be first, then the show statement
    Stops at the first underscore "_" or dot "." found
    Dashes "-" will be replaced by white spaces
    "int" will be replaced by "interface" or "interfaces"
    "nei" will be replaced by "neighbors"
    "det" will be replaced by "detail"
    "desc" or "descr" will be replaced by "description"

    The parser can also be specified explicitely with the "--parser" option

For a list of available parsers, please visit https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers

'''

import argparse
import sys
import os
import re
import json
import logging

from genie.conf.base import Device

# Default options
DEFAULT_OS = "nxos"
DEFAULT_DEVICENAME = "Device"
DEFAULT_PARSER = "show interface status"


def get_device_name_from_filename(filename, default=DEFAULT_DEVICENAME):
    '''
    Extract device name from filename
    '''
    # The device name starts at the beginning and ends at the first dash or underscore + "sh" (for "show")
    if filename == "<stdin>":
        device_name = DEFAULT_DEVICENAME
    else:
        filename = os.path.basename(filename)
        r = re.search(r"(.*)[-_]sh", filename)
        if r:
            device_name = r.groups()[0]
        else:
            device_name = DEFAULT_DEVICENAME
    return device_name

def get_parser_from_filename(filename, os=DEFAULT_OS):
    '''
    Infer Genie parser name from filename
    '''
    # The parser name starts at the first "show" statement and ends at the next underscore
    r = re.search(r"(show.*?)[_.]", filename)  
    if r:
        s = r.groups()[0]
    else:
        # Return the default parser DEFAULT_PARSER
        return DEFAULT_PARSER

    # Replace all dashes with spaces
    s = re.sub(r"-", " ", s)

    # Replace usual abreviations like "sh" or "int" with the full command
    s = re.sub(r"\bsho?\b", "show", s)
    s = re.sub(r"\brunn?\b", "running-config", s)
    s = re.sub(r"\bspan?\b", "spanning-tree", s)
    s = re.sub(r"\bneig?h?b?\b", "neighbors", s)
    s = re.sub(r"\bdet\b", "detail", s)
    s = re.sub(r"\bdescr?\b", "description", s)
    s = re.sub(r"\bsumm?\b", "summary", s)

    # Put the dash back in some of those commands
    s = re.sub(r"\running config\b", "running-config", s)
    s = re.sub(r"\spanning tree\b", "spanning-tree", s)
    s = re.sub(r"\bport channel\b", "port-channel", s)
    s = re.sub(r"\bfeature set\b", "feature-set", s)
    s = re.sub(r"\baccess list\b", "access-list", s)

    # Get alternative parser because no specific parser is available yet
    s = s.replace("show vpc brief", "show vpc")
    s = s.replace("show feature-set", "show feature")

    # Is it interface or interfaceS ?
    if "status" in s and "ios" in os:
        s = re.sub(r"\bint\b", "interfaces", s)
    else:
        s = re.sub(r"\bint\b", "interface", s)

    # Remove all newlines and whitespaces around the string, just in case
    s = s.strip()

    return s

def parse_cli_to_json(device_name, os, parser, cli_output):
    '''
    Parse CLI output to JSON data with Genie
    '''
    logging.info(f"[+] Parsing CLI from device {device_name} with parser \'{parser}\' (os={os})")
    device = Device(name=device_name, os=os)
    device.custom.abstraction = {"order": ["os"]}
    result = device.parse(parser, output=cli_output)
    return result


def main():
    '''
    Main program
    '''
    # Parse command line argument
    argparser = argparse.ArgumentParser(
        description="Read network device CLI output and print formatted JSON"
        )
    argparser.add_argument(
        "--infile",
        metavar="inputfile.txt",
        required=True,
        type=argparse.FileType("r"), 
        help="text file containing show command output (use '-' for stdin)"
        )
    argparser.add_argument(
        "--outfile", 
        metavar="FILENAME",
        help="save output to JSON file"
        )        
    argparser.add_argument(
        "--os",
        default=DEFAULT_OS,
        help=f"network OS which originated the output (default={DEFAULT_OS})"
        )
    argparser.add_argument(
        "--parser",
        #default=DEFAULT_PARSER,    # if we do this we can't overwrite the default parser later on
        help="Genie parser to use (default=infered from filename)"
        )
    argparser.add_argument(
        "--indent",
        default=2, 
        help="indentation for JSON output (default=2)"
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

    # If no Genie parser is specified we'll extract it from the filename or fallback to the default parser
    device_name = get_device_name_from_filename(infilename)
        
    # Select Genie parser or infer from filename
    if args.parser:
        parser = args.parser
    else:
        parser = get_parser_from_filename(infilename)

    # Parse CLI output to JSON data
    result = parse_cli_to_json(
        device_name=device_name, 
        os=args.os, 
        parser=parser,
        cli_output=cli_output
        )
    logging.info(f"[!] Done parsing device {device_name}, dumping JSON with indent {args.indent}")

    # Print JSON to file or stdout and quit
    if args.outfile:
        with open(args.outfile, "w") as f:
            f.write(json.dumps(result, indent=args.indent))
        logging.info(f"[!] Done writing JSON to {args.outfile}")
    else:
        print(json.dumps(result, indent=args.indent))


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
        sys.exit(1)
