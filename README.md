# cli2xls

Set of tools to convert raw CLI output from Cisco devices to human readable Excel spreadsheets.

### cli2json.py

Parse raw CLI output from network devices to structured JSON using the "NTC Templates" library.

### json2xls.py

Convert JSON files to Excel spreadsheets.


### cli2xls.py

Relies on the two aforementionned scripts to convert CLI output directly to Excel.


## Requirements / Getting started
```shell
pip install ntc-templates
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
- If no parser is specified, the parser/template will be infered from the filename using Regexes
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
