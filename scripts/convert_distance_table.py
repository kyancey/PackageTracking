"""This utility script converts the distance csv file to a python
   data structure and creates a .py file for usage in the project."""
import csv
import pprint


def get_address_from_name(address, dictionary):
    """Finds the address in the dictionary for the matching
       location name."""
    for i in range(len(dictionary["Name"])):
        if dictionary["Name"][i] == address:
            break
    return dictionary["Street"][i]


with open('Distance Table.csv', 'r', buffering=-1, encoding='utf-8-sig') as csvfile:
    csvdict = csv.DictReader(csvfile)
    jsondict = dict()

    # add field names to dict
    for x in csvdict.fieldnames:
        x = str.strip(x)
        jsondict[x] = list()

    # For each line, append the values to the end of the list stored in the dict field
    for line in csvdict:
        for field in csvdict.fieldnames:
            jsondict[str.strip(field)].append(str.strip(line[field]))
    csvfile.close()

    distance_hash = dict()
    for i in range(len(jsondict["Street"])):
        address1 = jsondict["Street"][i]
        for key in jsondict:
            if key == "Name" or key == "Street" or key == "Zip":
                continue
            elif jsondict[key][i] != "":
                address2 = get_address_from_name(key, jsondict)
                distance_hash[(address1, address2)] = float(jsondict[key][i])
                distance_hash[(address2, address1)] = float(jsondict[key][i])

    # Use pprint to format our data structure.
    repr_string = pprint.pformat(distance_hash, indent=2)

    # Write to file
    with open('../data/distance_data.py', 'w') as data_file:
        data_file.write("\"\"\"")
        data_file.write("Data structure containing distances between addresses.")
        data_file.write("\"\"\"\n")
        data_file.write("from HashTable import HashTable\n\n")
        data_file.write("distances = HashTable()\n")
        data_file.write("distances.update(" + repr_string + ")")
        data_file.close()
