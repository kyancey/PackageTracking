"""PackageTracking Program
   Author: Kyle Yancey
   Student ID: 003384372
   Date: 5/31/2021"""
import datetime
from functools import reduce

from DeliveryStatus import DeliveryStatus
from HashTable import HashTable
from Package import Package
from Truck import Truck
from data.package_data import packages


def print_package_status(package_list, time):
    """Given a list of  packages and a time period
       this function prints the status of each package
       at that time."""
    for package in package_list:
        package.print_status_at_time(time)


def create_trucks(num_trucks):
    """Create and return list of trucks"""
    trucks = list()
    for i in range(num_trucks):
        trucks.append(Truck())
    return trucks


def load_packages(trucks, package_data):
    """Add the packages to the assigned trucks and
       return packages hash table"""
    package_hashmap = HashTable()

    for package in package_data:
        # Convert numerical delivery status to enum for nicer comparison later on
        for name, member in DeliveryStatus.__members__.items():
            if package['Status'] == member.value:
                status = member

        # Add package to truck
        trucks[package['Truck'] - 1].add_package(Package(package['Package ID'],
                                                         package['Address'],
                                                         package['City'],
                                                         package['State'],
                                                         package['Zip'],
                                                         package['Deadline'],
                                                         package['Mass'],
                                                         status,
                                                         package['Truck'],
                                                         package['Delayed Until']))

    # Add to hashmap
    for truck in trucks:
        for package in truck.packages:
            package_hashmap[package.id] = package

    return package_hashmap


def display_menu(trucks, package_hashmap):
    """Present the user with options"""
    choice = None
    while choice != '0':
        print("Options")
        print("")
        print("0) Exit")
        print("1) All Package Status")
        print("2) Package Status")
        print("3) Truck Mileage")
        print("4) Total Mileage")
        choice = input()

        print("")
        if choice == "1":
            print("Enter a time after 0800 in military format. e.g. 0950")
            time = input()
            print("")
            hours = int(time[0:2])
            minutes = int(time[2:4])
            time = datetime.datetime(2021, 1, 1, hours, minutes, 0, 0)
            for truck in range(len(trucks)):
                print("Truck", truck + 1, "status:")
                trucks[truck].packages.sort(key=lambda x: x.id)
                print_package_status(trucks[truck].packages, time)
                print("")
        elif choice == "2":
            print("Enter package id number.")
            package_id = int(input())
            print("Enter a time after 0800 in military format. e.g. 0950")
            time = input()
            print("")
            hours = int(time[0:2])
            minutes = int(time[2:4])
            time = datetime.datetime(2021, 1, 1, hours, minutes, 0, 0)
            package_hashmap[package_id].print_status_at_time(time)
        elif choice == "3":
            print("Enter a number for the truck. (1-2)")
            truck_num = int(input()) - 1
            truck = trucks[truck_num]
            print("")
            print("Truck Mileage: ", truck.total_mileage())
            print("")
        elif choice == "4":
            print("")
            print("Total Mileage", reduce(lambda a, b: a.total_mileage() + b.total_mileage(), trucks))

        print("")


def create_package_list(package_hashmap):
    """Returns a list of all the packages
       sorted by the id number."""
    package_list = list()

    for key in package_hashmap:
        package_list.append(package_hashmap[key])
    package_list.sort(key=lambda x: x.id)

    return package_list


def main():
    """Main is the start of the program."""
    trucks = create_trucks(2)
    package_hashmap = load_packages(trucks, packages)
    create_package_list(package_hashmap)

    # Have each truck build their route
    for truck in trucks:
        truck.route()

    display_menu(trucks, package_hashmap)


main()
