#!usr/bin/env python3
import csv
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from operator import itemgetter
from pathlib import Path


def format_date(orig_date):
    """
    :param orig_date: e.g. 04/01/18
    :return: e.g. 2018-04-01
    """
    new_date_split = orig_date.split('/')
    fm_year = '20' + new_date_split[2]
    new_date = [fm_year, new_date_split[0], new_date_split[1]]
    return '-'.join(new_date)


def calc_card_collected(fees, deposited):
    """
    Card collected = deposited - fees

    NOTE: fees are negative numbers
    :param fees: e.g. -9.90
    :param deposited: e.g. 100.00
    :return: e.g. 109.9
    """
    return round(deposited - fees, 2)


def is_sorted(input_list):
    """
    Checks if sorted by sublist[0]
    :param input_list: e.g. [['3', 'hello'], ['2', 'hi'],
                            ['1', 'hey']]
    :return: False
    """
    return all(input_list[i][0] <= input_list[i+1][0] for i in range(len(input_list)-1))


def main():
    # Uncomment for production
    # ------------------------
    # Open a window to select the file (.csv)
    home = str(Path.home())
    root = Tk()
    root.withdraw()  # Hide empty window
    messagebox.showinfo(
        "Hola!", "Please select a Square deposit file\n\nIt should begin with: \"deposit-details-\"")
    root.filename = filedialog.askopenfilename(
        initialdir=home+"/Downloads", title="Select Square deposit file", filetypes=
        (("csv files", "*.csv"), ("all files", "*.*")))

    # info_button = Button(root, text="Please select Square deposit file")

    print(f"Opening file {root.filename}")
    square_filename = root.filename.split('/')[-1]
    abs_path_to_dir = '/'.join(root.filename.split('/')[:-1])

    # Open the csv file and create an array of each row
    raw_data = []
    with open(root.filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            raw_data.append(row)
    # ------------------------

    # # Uncomment for testing
    # # ------------------
    # home = str(Path.home())
    # test_file = home + "/Desktop/square deposits/deposit-details-2018-12-01-2019-01-01 - sb.csv"
    # print(f"Using test file {test_file}")
    # square_filename = test_file.split('/')[-1]
    # abs_path_to_dir = '/'.join(test_file.split('/')[:-1])
    # print(square_filename)
    # print(abs_path_to_dir, 'absolute path')
    #
    # # Open the csv file and create an array of each row
    # raw_data = []
    # with open(test_file, 'r') as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         raw_data.append(row)
    # # ------------------

    # Get first and last date of the csv contents
    first_date = raw_data[-1][0].split(',')[0]
    last_date = raw_data[1][0].split(',')[0]
    print("\nBeginning date:", first_date)
    print("Ending date:   ", last_date)

    # Format dates w/ year month then day
    first_date = format_date(first_date)
    last_date = format_date(last_date)

    # Format new filename
    location = str(raw_data[1][-1])
    new_square_filename = ('Square deposits for qb - ' + location + ' - ' +
                           first_date + ' to ' + last_date + '.csv')
    new_abs_path_to_file = (abs_path_to_dir + '/' + new_square_filename)

    # Iterate through raw data and add to dictionary
    iterraw_data = iter(raw_data)
    next(iterraw_data)  # skip headings
    square = {}
    for row in iterraw_data:
        deposit_id = row[8]
        deposit_date = row[0]

        total_collected = row[5]
        total_collected = ''.join(total_collected.split('$'))
        total_collected = float(''.join(total_collected.split(',')))

        fees = row[6]
        fees = float(''.join(fees.split('$')))

        deposited = row[7]
        deposited = ''.join(deposited.split('$'))
        deposited = float(''.join(deposited.split(',')))

        # print(deposit_date, total_collected, fees, deposited, deposit_id)

        # E.g. {'2Z66AKKQ0DJC8YKY12E74ZE9': ['12/31/18', 113.35, -3.13, 110.22]}
        if deposit_id not in square:
            square[deposit_id] = [deposit_date, total_collected, fees, deposited]
        else:
            square[deposit_id][1] += total_collected
            square[deposit_id][2] += fees
            square[deposit_id][3] += deposited

    # Round decimal places to 2
    for deposit_id in square:
        square[deposit_id][1] = round(square[deposit_id][1], 2)
        square[deposit_id][2] = round(square[deposit_id][2], 2)
        square[deposit_id][3] = round(square[deposit_id][3], 2)

    # Square deposit detail files come in reverse chronological order
    square_keys = list(square)
    square_keys.reverse()

    # Replace dictionary with list for sorting
    deposit_list = []
    for deposit_id in square_keys:
        date = square[deposit_id][0]
        total_collected = square[deposit_id][1]
        fees = square[deposit_id][2]
        deposited = square[deposit_id][3]
        card_collected = calc_card_collected(fees, deposited)
        deposit_list.append(
            [date, deposit_id, total_collected, card_collected, fees, deposited])
        del square[deposit_id]

    if not is_sorted(deposit_list):
        deposit_list.sort(key=itemgetter(0))  # sort by date

    print(f"\nWriting data to {new_abs_path_to_file}..")
    # Write deposit list to .csv with headings
    with open(new_abs_path_to_file, mode='w') as square_deposits:
        square_writer = csv.writer(square_deposits, delimiter=',', quotechar='"')
        square_writer.writerow(
            ['Deposit Date', 'Deposit ID', 'Total Collected', 'Card Collected', 'Fees', 'Deposited'])

        for row in deposit_list:
            print(row)
            square_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])


if __name__ == '__main__':
    main()

