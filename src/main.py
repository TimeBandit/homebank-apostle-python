import csv
from src.providers.starling import parse_line
from src.utils.display import display_rows_in_terminal
import argparse


def read_starling_csv(input_file):
    """Read the Starling CSV file and return a list of parsed rows"""
    parsed_rows = []
    with open(input_file, newline='') as csvfile:
        dicReader = csv.DictReader(csvfile)
        for row in dicReader:
            parsed_data = {
                key.value: value for key,
                value in parse_line(row).items()
            }
            parsed_rows.append(parsed_data)
    return parsed_rows


def write_homebank_csv(output_file, rows):
    """Write the parsed rows to a new HomeBank CSV file"""
    if not rows:
        return

    fieldnames = list(rows[0].keys())  # Get headers from first row

    with open(output_file, 'w', newline='') as csvfile:
        dict_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(rows)

    # Display in terminal
    display_rows_in_terminal(rows)


def convert_starling_to_homebank(input_file, should_write=False):
    """Convert Starling CSV to HomeBank format"""
    parsed_rows = read_starling_csv(input_file)

    # Always display in terminal
    display_rows_in_terminal(parsed_rows)

    # Write to file only if requested
    if should_write:
        # Generate output filename based on input filename
        output_file = input_file.rsplit('.', 1)[0] + '_converted.csv'
        write_homebank_csv(output_file, parsed_rows)
        print(f"\nFile written to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Convert Starling Bank CSV to HomeBank format'
    )
    parser.add_argument(
        'input_file',
        help='The Starling Bank CSV file to convert'
    )
    parser.add_argument(
        '--write',
        action='store_true',
        help='Write the output to a CSV file (default: only display in terminal)'
    )

    args = parser.parse_args()
    convert_starling_to_homebank(args.input_file, args.write)


if __name__ == "__main__":
    main()
