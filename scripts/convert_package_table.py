"""This utility script converts the package csv to a python
   data structure and writes a .py file for usage in the project."""
import csv

import DeliveryStatus

with open('Package File.csv', 'r', buffering=-1, encoding='utf-8-sig') as csvfile:
    csvdict = csv.DictReader(csvfile)
    jsonlist = list()

    # Create the package dicts and add them to a list
    for line in csvdict:
        x = dict()
        x['Package ID'] = int(line['Package ID'])
        x['Address'] = line['Address']
        x['Delayed Until'] = line['Delayed Until']
        x['Truck'] = int(line['Truck'])
        x['Mass'] = int(line['Mass'])
        x['Deadline'] = line['Deadline']
        x['Zip'] = line['Zip']
        x['City'] = line['City']
        x['State'] = line['State']

        if line['Instructions'] == 'standard' and line['Deadline'] != '':
            x['Status'] = DeliveryStatus.DeliveryStatus.at_hub.value
        elif line['Instructions'] == 'standard':
            x['Status'] = DeliveryStatus.DeliveryStatus.out_for_delivery.value
        elif line['Instructions'] == 'delayed arrival':
            x['Status'] = DeliveryStatus.DeliveryStatus.delayed_arrival.value
        elif line['Instructions'] == 'awaiting address update':
            x['Status'] = DeliveryStatus.DeliveryStatus.awaiting_address_update.value

        jsonlist.append(x)

csvfile.close()

# Build up the data structure using our personal HashTable class.
repr_string = "["
for dictionary in jsonlist:
    repr_string += "HashTable(2, " + repr(dictionary) + "),\n"
repr_string += "]"

# Write to file
with open('../data/package_data.py', 'w') as data_file:
    data_file.write("from HashTable import HashTable\n\n")
    data_file.write("packages = " + repr_string)
    data_file.close()
    del data_file, jsonlist
