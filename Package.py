"""Package Class"""
import datetime
from DeliveryStatus import DeliveryStatus
from HashTable import HashTable


class Package:
    """The Package class stores package info and provides methods
       for maintaining status history."""
    def __init__(self, package_id, address, city, state, zip_code, deadline, mass, status, truck, delay_until):
        self.id = package_id
        self.address = address
        self.truck = truck
        self.initial_status = status
        self.mass = mass
        self.zip = zip_code
        self.city = city
        self.state = state
        self.status = status

        self.delay_until = delay_until
        if self.delay_until != "":
            hour = int(delay_until.split(':')[0])
            minute = int(delay_until.split(':')[1])
            self.delay_until = datetime.datetime(2021, 1, 1, hour, minute, 0, 0)

        self.deadline = deadline
        if self.deadline == "EOD":
            # Set EOD packages to have a delivery deadline of 5:00 PM
            self.deadline = datetime.datetime(2021, 1, 1, 17, 0, 0, 0)
        else:
            hour = int(deadline.split(':')[0])
            minute = int(deadline.split(':')[1])
            self.deadline = datetime.datetime(2021, 1, 1, hour, minute, 0, 0)

        self.status_history = list()

    def clear_status_history(self):
        """Erase the status history."""
        self.status_history = list()

    def get_status_at_time(self, time):
        """Returns the last status before the given time."""
        for item in self.status_history:
            if item['start_time'] <= time < item['end_time']:
                return item['status']

    def change_status(self, status, time):
        """Changes the status of the package and adds an
           entry to status history."""
        self.status = status
        status_item = HashTable(2)
        status_item.update({'status': status, 'time': time})
        self.status_history.append(status_item)

    def print_status_at_time(self, status_time):
        """Prints out the status of the package at the given time."""
        last_status = None
        # Find the most recent status that isn't past the given time.
        for status in self.status_history:
            if status["time"] < status_time:
                last_status = status
            else:
                break

        # Choose what status text to print
        status_text = ""
        if last_status["status"] == DeliveryStatus.at_hub:
            status_text = "At the Hub"
        elif last_status["status"] == DeliveryStatus.out_for_delivery:
            status_text = "Out for Delivery"
        elif last_status["status"] == DeliveryStatus.delivered:
            status_text = "Delivered at " + str(last_status['time'].time())
        elif last_status["status"] == DeliveryStatus.delayed_arrival:
            status_text = "Arrival Delayed"

        print("Package ID:", f'{self.id},', "Address:", f'{self.address},', status_text)
