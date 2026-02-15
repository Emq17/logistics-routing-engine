import csv
from package import Package
from distance import DistanceTable


def load_packages(path):
    # Load packages data from packages.csv into a list of Package objects
    packages = []

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Pull fileds by header name (keeps the loader resilient to column order)
            package_id = int(row["Package ID"])
            address = row["Address"].strip()
            city = row["City"].strip()
            zip_code = str(row["Zip"]).strip()
            deadline = row["Delivery Deadline"].strip()
            weight = str(row["Weight (Kgs)"]).strip()
            note = row.get("Special Notes", "").strip()

            # Store everything in a Package object so status/time can be updated later
            packages.append(
                Package(package_id, address, city, zip_code, deadline, weight, note)
            )

    return packages


def _to_float(value):
    # Convert a distance cell into a float
    # Empty cells in the CSV become None (spreadsheet formatted only half filled)
    if value is None:
        return None

    s = str(value).strip()
    if s == "":
        return None

    try:
        return float(s)
    except ValueError:
        return None


def _clean_location(text):
    # Normalize location strings so they match across packages + distance table
    if text is None:
        return ""

    s = str(text).replace("\n", " ").strip()

    # Remove zip in parentheses: "195 W Oakland Ave (84115)" -> "195 W Oakland Ave"
    if "(" in s:
        s = s.split("(")[0].strip()

    # Normalize spacing
    s = " ".join(s.split())
    return s


def load_distances(path):
    # Load distance table CSV into a DistanceTable object (locations + 2D matrix)
    rows = []

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for r in reader:
            if r and any(str(cell).strip() for cell in r):
                rows.append(r)

    # Keep only rows that actually contain numeric distance values
    data_rows = []
    for r in rows:
        if len(r) >= 3 and _to_float(r[2]) is not None:
            data_rows.append(r)

    locations = []
    matrix = []

    for r in data_rows:
        raw_loc = r[1] if len(r) > 1 else r[0]
        loc = _clean_location(raw_loc)

        locations.append(loc)

        vals = [_to_float(x) for x in r[2:]]
        matrix.append(vals)

    # The first row is the hub row in this dataset
    if locations:
        locations[0] = "HUB"

    return DistanceTable(locations, matrix)