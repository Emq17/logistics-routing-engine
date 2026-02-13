class Package:
    def __init__(self, package_id, address, city, zip_code, deadline, weight, note=""):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.note = note

        self.status = "At hub"
        self.load_time = None
        self.delivery_time = None

    def set_en_route(self, time):
        self.status = "En route"
        self.load_time = time

    def set_delivered(self, time):
        self.status = "Delivered"
        self.delivery_time = time

    def status_at(self, time):
        if self.load_time is None:
            return "At hub"

        if time < self.load_time:
            return "At hub"

        if self.delivery_time is None or time < self.delivery_time:
            return "En route"

        return "Delivered"

    def __repr__(self):
        return f"Package({self.package_id}, {self.address}, {self.status})"