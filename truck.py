class Truck:
    SPEED_MPH = 18.0
    MAX_PACKAGES = 16

    def __init__(self, truck_id, start_time_minutes=8 * 60):
        # Basic truck state used for the delivery simulation
        self.id = truck_id
        self.time = float(start_time_minutes)       # minutes since midnight
        self.start_time = float(start_time_minutes) # When this truck is allowed to leave the hub
        self.location = "HUB"
        self.miles = 0.0
        self.packages = []

    def load(self, package):
        # Load a package onto the truck (capacity limit = 16)
        if len(self.packages) >= Truck.MAX_PACKAGES:
            raise ValueError("Truck is full")
        
        self.packages.append(package)
        
        # Record which truck the package is assigned to
        # Status changes happen during the simulation (depart/delivered), not at load time
        package.truck_id = self.id  

    def drive_to(self, destination, distance_table):
        # Move from current location to destination, updating mileage and time
        dist = distance_table.distance(self.location, destination)

        self.miles += dist

        # Convert distance into minutes using the fixed 18 MPH speed
        minutes = (dist / Truck.SPEED_MPH) * 60.0
        self.time += minutes
        self.location = destination

    def return_to_hub(self, distance_table):
        # End the route by driving back to the hub
        self.drive_to("HUB", distance_table)