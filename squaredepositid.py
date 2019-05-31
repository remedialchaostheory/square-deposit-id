#!usr/bin/env python3
import csv
from tkinter import filedialog
from tkinter import *
import operator

# --------------------

def main():
    # Opens a window to select the file (.csv)
    root = Tk()
    root.filename = filedialog.askopenfilename(
        initialdir = "/",title = "Select file",filetypes =
        (("csv files","*.csv"),("all files","*.*")))
    print(root.filename)
    base_fn = root.filename.split('/')[-1]
    base_path = '/'.join(root.filename.split('/')[:-1])
    print(base_fn)
    print(base_path, 'base_path')
    original_fn = base_fn

    # ---------------------

    # Open the csv file
    # Create an array of each row
    raw_data = []
    with open(root.filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            raw_data.append(row)

    # Get first and last date of the CSV contents
    first_date = raw_data[-1][0].split(',')[0]
    last_date = raw_data[1][0].split(',')[0]
    print('first ', first_date)
    print('last ', last_date)

    def format_date(orig_date):
        # e.g. orig_date = 04/01/18
        # output = 2018-04-01
        new_date_split = orig_date.split('/')
        fm_year = '20' + new_date_split[2]
        new_date = [fm_year, new_date_split[0], new_date_split[1]]
        return '-'.join(new_date)


    # Format dates w/ year month then day
    first_date = format_date(first_date)
    last_date = format_date(last_date)

    # Format new filename
    new_fn = (base_path + '/' + 'square-qb-deposits-' +
              first_date + '-' + last_date + '.csv')

    # deposit_date = [0]
    # collected = [5]
    # fees = [6]
    # deposited = [7]
    # deposit_id = [8]

    # Iterate through raw_data and save
    square = {}
    deposit_date = ''
    collected = 0
    fees = 0
    deposited = 0
    deposit_id = 0

    iterraw_data = iter(raw_data)
    next(iterraw_data)
    for row in iterraw_data:
        deposit_id = row[8]
        deposit_date = row[0]

        collected = row[5]
        collected = ''.join(collected.split('$'))
        collected = float(''.join(collected.split(',')))

        fees = row[6]
        fees = float(''.join(fees.split('$')))

        deposited = row[7]
        deposited = ''.join(deposited.split('$'))
        deposited = float(''.join(deposited.split(',')))

        # print(deposit_date, collected, fees, deposited, deposit_id)

        if deposit_id not in square:
            square[deposit_id] = [deposit_date, collected, fees, deposited]
        else:
            square[deposit_id][1] += collected
            square[deposit_id][2] += fees
            square[deposit_id][3] += deposited


        # square[deposit_id]['collected'] = square[deposit_id]['collected'] + collected

    # Round decimal places to 2
    for id in square:
        square[id][1] = round(square[id][1], 2)
        square[id][2] = round(square[id][2], 2)
        square[id][3] = round(square[id][3], 2)

    print(square)

    # Write data to new .csv file
    with open(new_fn, mode='w') as square_deposits:
        square_writer = csv.writer(square_deposits, delimiter=',', quotechar='"')

        for id in square:
            square_writer.writerow(
                [square[id][0], id, square[id][1], square[id][2], square[id][3]])

    square_deposits.close()

    # TODO - can refactor this to only open file once by sorting beforehand
    # Reopen file to sort by date
    reader = csv.reader(open(new_fn), delimiter=";")
    sorted_list = sorted(reader, key=operator.itemgetter(0), reverse=False)

    # Write sorted data with headings
    with open(new_fn, mode='w') as square_deposits:
        square_writer = csv.writer(square_deposits, delimiter=',', quotechar='"')
        square_writer.writerow(
            ['Deposit Date', 'Deposit ID', 'Collected', 'Fees', 'Deposited'])

        for r in sorted_list:
            row = r[0].split(',')
            print(row)
            square_writer.writerow([row[0], row[1], row[2], row[3], row[4]])

    print(sorted_list)

if __name__ == '__main__':
    main()

