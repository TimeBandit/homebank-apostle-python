# Convert Starling Bank CSV to HomeBank format

```bash
positional arguments:
input_file The Starling Bank CSV file to convert

options:
-h, --help show this help message and exit
--write Write the output to a CSV file (default: only display in terminal)
```

## Installation

To run this from terminal folder first run once ` pip install -e .` from the
project root

## Running

```bash
hba-python [-h] [--write] input_file
```

By default it will out the converted data to a table in the terminal.
