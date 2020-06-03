# cli2xls

Set of tools to convert raw CLI output from Cisco devices to human readable Excel spreadsheets.

### cli2json.py

Parse raw CLI output from network devices to structured JSON using the Cisco pyATS/Genie library.

### json2xls.py

Convert JSON files to Excel spreadsheets. Relies on a set of custom parsers located in the "jsonparsers" subdirectory.


### cli2xls.py (work in progress)

Relies on the two aforementionned scripts to convert CLI to JSON and then directly to XLS.

It can also colorize the spreadsheets using xlscolors.py.

## Requirements / Getting started
```shell
pip install pyats[library]
pip install openpyxl
```
```shell
python cli2xls.py network-device_show-cdp-nei.txt --outfile NetworkDevice.xlsx
```

## Usage

Use ```--help``` to display usage and options.

## License

Author: David Paneels

This code is private and for internal use only.
