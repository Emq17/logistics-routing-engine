class Truck:
    SPEED_MPH = 18.0
    MAX_PACKAGES = 16

    def __init__(self, truck_id, start_time_minutes=8 * 60):
        self.id = truck_id
        self.time = start_time_minutes  # minutes since midnight
        self.location = "HUB"
        self.miles = 0.0
        self.packages = []

    def load(self, package):
        if len(self.packages) >= Truck.MAX_PACKAGES:
            raise ValueError("Truck is full")
        self.packages.append(package)
        package.truck_id = self.id

    def drive_to(self, destination, distance_table):
        dist = distance_table.distance(self.location, destination)

        self.miles += dist
        minutes = (dist / Truck.SPEED_MPH) * 60.0
        self.time += minutes
        self.location = destination

    def return_to_hub(self, distance_table):
        self.drive_to("HUB", distance_table)