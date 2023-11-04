#!/usr/bin/env python3
"""Allows input of names, timed, which get saved to a CSV file.
Name
Seconds: Seconds to come up with the current name
MinuteIndex: Point at which the current name came up, in minutes
"""
import argparse
import csv
import os
import time


SAVE_FILE = 'listofnames.csv'
TIME_LIMIT = 10  # minutes
QUIT = '/x'


def parse_args():
    """Parse user arguments and return as parser object.

    Returns:
        Parser object with arguments as attributes.
    """
    parser = argparse.ArgumentParser(description='Nombres.')
    parser.add_argument(
        '-p', '--pressure', action='store_true',
        help='Pressure mode; shows elapsed times in seconds.')
    parser.add_argument(
        '-s', '--save_file', default=SAVE_FILE,
        help='Name of CSV file into which to save names and times.')
    parser.add_argument(
        '-t', '--time_limit', default=TIME_LIMIT, type=int,
        help='Number of minutes to allow input.')
    args = parser.parse_args()
    return args


def validate_file(file_name=SAVE_FILE):
    """Ensure that the file name desired should be used.

    Args:
        file_name: File name desired.

    Returns:
        file_name: Final file name to be used (may be same as input).
    """
    while os.path.exists(file_name):
        print(f'File "{file_name}" exists.')
        response = input('Do you wish to over-write the file? [y/N] ')
        if response.strip().lower().startswith('y'):
            break
        file_name = ''
        while file_name == '':
            file_name = input('Name of file to save to: ').strip()
            if file_name and not file_name.lower().endswith('.csv'):
                file_name += '.csv'
        print(f'New file name: "{file_name}"')
    return file_name


def save_data(data, save_file):
    """Save the list (dictionary) of names to a CSV file all at once.

    Args:
        data: Dictionary of names; names[name] = (seconds, total_time)
        save_file: Name of file into which to save data.
    """
    with open(save_file, 'w', encoding='utf-8') as file_handle:
        csv_writer = csv.writer(file_handle)
        csv_writer.writerow(['Name', 'Seconds', 'MinuteIndex'])
        for name, values in data.items():
            csv_writer.writerow([name, values[0], values[1]])


def main():
    """Does the work.
    """
    names = {}  # unique names only
    save_file = validate_file(ARGS.save_file)

    time_total = minute = 0  # set timers to 0
    keep_going = True
    input('Press <enter> to start typing names.')
    time_previous = time.time()
    while keep_going:
        name = ''
        while name == '':
            try:
                name = input(f'Name ("{QUIT}" to quit): ').strip()
            except KeyboardInterrupt:
                name = QUIT
                print()
        if name == QUIT:
            break
        name = name.title()

        time_now = time.time()  # seconds
        time_elapsed = time_now - time_previous  # time for current name
        time_total += time_elapsed  # time since start of program
        minutes_total = time_total / 60
        time_previous = time_now
        if ARGS.pressure:
            print(f'  ## {minutes_total:.2f} minutes have elapsed.')
        elif int(minutes_total) > minute:
            minute = int(minutes_total)
            print(f'  ## {minute} minute{"s" if minute != 1 else ""} elapsed.')
        if name in names:
            print(f'  ## ## "{name}" was already entered.')
            time_elapsed += names[name][0]
        names[name] = time_elapsed, minutes_total

        keep_going = minutes_total < ARGS.time_limit
    save_data(names, save_file)
    print(f'Time is up! {len(names)} names entered.')


if __name__ == '__main__':
    ARGS = parse_args()
    main()
