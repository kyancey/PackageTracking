"""Truck Class"""
import datetime
from DeliveryStatus import DeliveryStatus
from HashTable import HashTable
from Package import Package
from data.distance_data import distances


class Truck:
    """The Truck class contains methods for storing package
       data, calculating mileage, and creating delivery routes."""
    def __init__(self):
        self.packages = list()
        self.package_route = list()
        self.distances = distances
        self.travel_speed = 18
        self.mileage = 0

    def add_package(self, package):
        """Adds package to truck."""
        self.packages.append(package)

    def route(self):
        """The route method is responsible for turning the assigned
           packages list into a delivery route. This is primarily
           achieved through a priority system. Priority is based on
           time first and distance second. There are two special
           cases: 1) Packages that arrive at the hub later 2) Packages
           that are awaiting address changes."""
        start_time = datetime.datetime(2021, 1, 1, 8, 0, 0, 0)
        current_time = datetime.datetime(2021, 1, 1, 8, 0, 0, 0)
        load_time = datetime.datetime(2021, 1, 1, 8, 0, 0, 0)
        current_address = "Pat Garrett University"  # Start at hub
        hub = Package(-1, "Pat Garrett University", "", "", "", "23:00", "",
                      DeliveryStatus.out_for_delivery, "1", "")  # Dummy package for hub
        unassigned_packages = self.packages.copy()
        delivery_count = 0  # tracks number of packages delivered by the truck without going back to the hub
        delivery_limit = 16

        # Loop over unassigned packages, removing one each cycle
        # Leave packages in for an additional cycle when you have
        # to pick them up at the HUB
        while len(unassigned_packages) != 0:
            # Make sure we haven't delivered more than the trucks limit
            if delivery_count >= delivery_limit:
                # Return to hub
                self.add_package_to_route(current_time, current_address, hub)
                delivery_count = 0
                load_time = self.package_route[-1]['time']

            candidate_packages = self.get_next_deadline_group(unassigned_packages)
            next_package = self.get_nearest_package(current_address, candidate_packages)

            # If the package is awaiting an address update, do a quick check for a better match
            if next_package.status == DeliveryStatus.awaiting_address_update:
                # If it's not time yet, look for another package.
                discards = list()
                if next_package.delay_until > current_time:
                    while next_package.status == DeliveryStatus.awaiting_address_update:
                        discards.append(next_package)
                        unassigned_packages.remove(next_package)
                        candidate_packages = self.get_next_deadline_group(unassigned_packages)
                        next_package = self.get_nearest_package(current_address, candidate_packages)

                # Add the discarded packages back
                for p in discards:
                    unassigned_packages.append(p)

            # If next package is still awaiting address, that means it's past time to deliver it.
            if next_package.status == DeliveryStatus.awaiting_address_update:
                next_package.delay_until = ""

                next_package.change_status(DeliveryStatus.at_hub, start_time)
                next_package.change_status(DeliveryStatus.out_for_delivery, load_time)

            # If the package still hasn't shown up, look for a better match.
            if next_package.status == DeliveryStatus.delayed_arrival:
                # If it's not time yet, look for another package.
                discards = list()
                if next_package.delay_until > current_time:
                    while next_package.status == DeliveryStatus.delayed_arrival:
                        discards.append(next_package)
                        unassigned_packages.remove(next_package)
                        candidate_packages = self.get_next_deadline_group(unassigned_packages)
                        next_package = self.get_nearest_package(current_address, candidate_packages)

                # Add the discarded packages back
                for p in discards:
                    unassigned_packages.append(p)

            if next_package.status == DeliveryStatus.delayed_arrival:
                # Set it's initial status up to this point
                next_package.change_status(DeliveryStatus.delayed_arrival, start_time)
                next_package.change_status(DeliveryStatus.at_hub, next_package.delay_until)

                # Go back to hub to pick it up
                self.add_package_to_route(current_time, current_address, hub)
                delivery_count = 0

                load_time = self.package_route[-1]["time"]

                # Make sure we update the current address and time
                current_address = hub.address
                current_time = self.package_route[-1]['time']

                # Change delivery status so we can now treat this package like one on the truck
                next_package.change_status(DeliveryStatus.out_for_delivery, load_time)
                next_package.delay_until = ""
            else:
                # For any non-delayed arrival package, we just can just add it to the route
                # and remove it from the unassigned list
                self.add_package_to_route(current_time, current_address, next_package)
                unassigned_packages.remove(next_package)
                delivery_count += 1

                # Make sure we update the current address and time
                current_address = next_package.address
                current_time = self.package_route[-1]['time']

                # Update the package status
                next_package.change_status(DeliveryStatus.at_hub, start_time)
                next_package.change_status(DeliveryStatus.out_for_delivery, load_time)
                next_package.change_status(DeliveryStatus.delivered, current_time)

        # Return to Hub
        self.add_package_to_route(current_time, current_address, hub)

    def get_next_deadline_group(self, unassigned_packages):
        """Return a set containing the group of packages that are next based on time."""

        # find earliest time
        min_time = datetime.datetime(2021, 1, 1, 23, 59, 59, 0)
        for package in unassigned_packages:
            if package.delay_until != "":
                package_time = package.delay_until
            else:
                package_time = package.deadline
            if package_time < min_time:
                min_time = package_time

        # find all packages that share earliest time
        deadline_group = list()
        for package in unassigned_packages:
            if package.delay_until != "" and package.delay_until == min_time:
                deadline_group.append(package)
            else:
                if package.deadline == min_time:
                    deadline_group.append(package)

        return deadline_group

    def get_nearest_package(self, current_address, candidate_packages) -> Package:
        """Returns the nearest package in a set of packages given the current address"""
        smallest_distance = None
        smallest_package = None

        for package in candidate_packages:
            # Only runs for first package
            if smallest_distance is None:
                smallest_distance = distances[(current_address, package.address)]
                smallest_package = package

            if distances[(current_address, package.address)] < smallest_distance:
                smallest_distance = distances[(current_address, package.address)]
                smallest_package = package

        return smallest_package

    def add_package_to_route(self, current_time, current_address, next_package):
        """Adds the given package to the delivery route and assigns the calculated
           travel time based on how long it would take to arrive from the current
           address. There is one special case where the package to be delivered is
           the hub. In that instance, the routing event type is a pickup instead of
           a delivery.
           """
        # Get travel distance and calculate arrival time.
        travel_distance = distances[(current_address, next_package.address)]
        self.mileage += travel_distance
        travel_time = travel_distance / self.travel_speed
        travel_time = datetime.timedelta(hours=travel_time)
        arrival_time = current_time + travel_time

        route_item = HashTable(3)
        # Determine type of activity
        if next_package.id != -1:
            route_item.update({'type': 'delivery', 'time': arrival_time, 'package': next_package})
            self.package_route.append(route_item)
        else:
            route_item.update({'type': 'pickup', 'time': arrival_time, 'package': next_package})
            self.package_route.append(route_item)

    def total_mileage(self):
        """Returns the total miles traveled by the truck.
           Note: Mileage is unrelated to total time traveled
           because the truck stops and waits for a few packages."""
        return self.mileage
