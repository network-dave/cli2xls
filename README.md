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
python cli2xls.py --infile network-device_show-cdp-nei.txt --outfile NetworkDevice.xlsx
```

## Usage (please read!)

Use ```--help``` to display usage and options.

- The only mandatory argument is ```--infile```
- '-' can be used in place of the filename to read from STDIN
- If no ```--outfile``` is specified, the script will create a new file based on the ```device_name```, or simply print to STDOUT
- If no parser is specified, the Genie/JSON parser will be infered from the filename using Regexes
- The ```jsonparsers/``` directory and subdirectory must be present to parse JSON to Excel tables
- JSON parsers are simple Python modules which implement a ```parse()``` function that returns a list of lists (first item is thus the column header)
- If no module exists for the selected parser, the ```default.py``` module is used, which parses all the leaf objects. This works for some commands like ```show interface status```
- If the Excel file/workbook exists, the new spreadsheet will be added at the end, if not a new Excel file will be created
- The title of the new spreadsheet is the name of the parser
- ```--verbose``` prints some additional information to STDERR

## Tips & Tricks

To process batches of files, use something like:
```shell
find ./*.txt -exec sh -c "python cli2xls.py --infile {}" \;
```


## License

Author: David Paneels

This code is private and for internal use only.
