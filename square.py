import csv
import glob


# import Tkinter as tk
# r=tk.Tk()
# '''
# widgets are added here
# '''
# r.title('Process Deposits')
# button = tk.Button(r, text='Stop', width=25, command=r.destroy)
# button.pack()
# r.mainloop()

# --------------------
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog

root = Tk()
root.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
print (root.filename)
base_fn = root.filename.split('/')[-1]
base_path = '/'.join(root.filename.split('/')[:-1])
print base_fn
print base_path, 'base_path'
original_fn = base_fn
# ---------------------

# Open the csv file
# Create an array of each row
raw_data = []
with open(root.filename, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        raw_data.append(row)

# Get first and last date of the CSV contents
first_date = raw_data[-1][0].split(',')[0]
last_date = raw_data[1][0].split(',')[0]
print 'fisrt', first_date
print 'last', last_date

# e.g. orig_date = 04/01/18
# output = 2018-04-01
def format_date(orig_date):
    new_date_split = orig_date.split('/')
    fm_year = '20' + new_date_split[2]
    new_date = [fm_year, new_date_split[0], new_date_split[1]]
    return '-'.join(new_date)


# Format dates w/ year month then day
first_date = format_date(first_date)
last_date = format_date(last_date)

# Format new filename
new_fn = base_path + '/' + 'square-qb-deposits-' + first_date + '-' + last_date + '.csv'

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

    # print deposit_date, collected, fees, deposited, deposit_id

    if deposit_id not in square:
        square[deposit_id] = [deposit_date, collected, fees, deposited]
    else:
        square[deposit_id][1] += collected
        square[deposit_id][2] += fees
        square[deposit_id][3] += deposited


    # square[deposit_id]['collected'] = square[deposit_id]['collected'] + collected

# Round decimal places to 2
for k in square:
    square[k][1] = round(square[k][1], 2)
    square[k][2] = round(square[k][2], 2)
    square[k][3] = round(square[k][3], 2)

print square

with open(new_fn, mode='w') as square_deposits:
    square_writer = csv.writer(square_deposits, delimiter=',', quotechar='"')

    for k in square:
        square_writer.writerow([square[k][0], k, square[k][1], square[k][2], square[k][3]])

square_deposits.close()

import operator
# Sort by date
reader = csv.reader(open(new_fn), delimiter=";")
sorted_list = sorted(reader, key=operator.itemgetter(0), reverse=False)

with open(new_fn, mode='w') as square_deposits:
    square_writer = csv.writer(square_deposits, delimiter=',', quotechar='"')
    square_writer.writerow(['Deposit Date', 'Deposit ID', 'Collected', 'Fees', 'Deposited'])

    # first_date = ''
    # last_count = len(sorted_list) - 1
    # count = 0
    for r in sorted_list:
        row = r[0].split(',')
        print row
        square_writer.writerow([row[0], row[1], row[2], row[3], row[4]])

print sorted_list



# iterraw_data = iter(raw_data)
# next(iterraw_data)
# for row in iterraw_data:
#     deposit_date = row[0]
#     collected = row[5]
#     collected = float(collected[1:-1])
#     fees = row[6]
#     deposited = row[7]
#     deposit_id = row[8]
#     print deposit_date, collected, fees, deposited, deposit_id
#     square[deposit_id] = {}
#     # square[deposit_id]['collected'] = square[deposit_id]['collected'] + collected
#     print collected
#     if 'collected' not in square[deposit_id]:
#         square[deposit_id]['collected'] = collected
#         # print 'hi'
#     else:
#         square[deposit_id]['collected'] += collected
#         print 'no'
#     print collected
#     # square[deposit_id]['collected'] += collected
#     # square[deposit_id]['collected'] = 0.0


