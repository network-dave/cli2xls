# cli2xls

Set of tools to convert raw CLI output from Cisco devices to human readable Excel spreadsheets.

### cli2json.py

Parse raw CLI output from network devices to structured JSON, using the NTC-Templates library.

### json2xls.py

Convert JSON files to Excel spreadsheets.

### cli2xls.py

Relies on the two aforementionned scripts to convert CLI output directly to Excel.

### cli2singlexls.py

Parses a group of text files into a single Excel spreadsheet (works best for a single command output from all devices)

## Requirements / Getting started
```shell
pip install ntc-templates
pip install openpyxl
```

If you need to write custom templates, you can also fork the ntc-templates repository from Github and install the module from there:
```shell
git clone https://github.com/networktocode/ntc-templates.git
pip install -e ntc-templates/[dev]
```

```shell
python cli2xls.py --infile network-device_show-cdp-nei.txt --outfile NetworkDevice.xlsx
```



## Usage

Use ```--help``` to display usage and options.

- '-' can be used in place of the filename to read from STDIN
- If no ```--outfile``` is specified, the script will create a new file based on the ```device_name```, or simply print to STDOUT
- If no parser is specified, the parser/template will be infered from the filename using Regexes
- If the Excel file/workbook exists, the new spreadsheet will be added at the end, if not a new Excel file will be created
- The title of the new spreadsheet is the name of the parser/template
- ```--verbose``` prints some additional information to STDERR

## Tips & Tricks

To process batches of files, use something like:
```shell
find ./*.txt -exec sh -c "python cli2xls.py --infile {}" \;
```


## License

Copyright (C) 2020 David Paneels

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

https://www.gnu.org/licenses/gpl-3.0.html
