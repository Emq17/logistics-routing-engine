class Package:
    def __init__(self, package_id, address, city, zip_code, deadline, weight, note):
        self.id = package_id
        self.address = address
        self.city = city
        self.zip = zip_code
        self.deadline = deadline
        self.weight = weight
        self.note = note

        self.status = "At hub"
        self.delivery_time = None
        self.truck_id = None

    def mark_en_route(self, truck_id):
        self.status = "En route"
        self.truck_id = truck_id

    def mark_delivered(self, time_str):
        self.status = "Delivered"
        self.delivery_time = time_str

    def __repr__(self):
        delivered = f", delivered {self.delivery_time}" if self.delivery_time else ""
        return f"Package({self.id}, {self.address}, {self.status}{delivered})"