class Package:
    def __init__(self, package_id, address, city, zip_code, deadline, weight, note):
        self.id = package_id
        self.address = address
        self.city = city
        self.zip = zip_code
        self.deadline = deadline
        self.weight = weight
        self.note = note

        # These get updated during the delivery simulation
        self.status = "At hub"      # At hub -> En route -> Delivered
        self.delivery_time = None   # AM/PM string once delivered
        self.truck_id = None        # Which truck the package was loaded on

    def mark_en_route(self, truck_id):
        # Called when the package is loaded onto a truck/leaves the hub
        self.status = "En route"
        self.truck_id = truck_id

    def mark_delivered(self, time_str):
        # Called at delivery time when the truck reaches the package address
        self.status = "Delivered"
        self.delivery_time = time_str

    def __repr__(self):
        # For quick debugging prints
        delivered = f", delivered {self.delivery_time}" if self.delivery_time else ""
        return f"Package({self.id}, {self.address}, {self.status}{delivered})"