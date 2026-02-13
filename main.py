# Student ID: 010306042

from loader import load_packages, load_distances
from truck import Truck


def minutes_to_ampm(total_minutes):
    total_minutes = int(round(total_minutes))
    h = (total_minutes // 60) % 24
    m = total_minutes % 60

    suffix = "AM"
    hour12 = h
    if h == 0:
        hour12 = 12
    elif h == 12:
        suffix = "PM"
        hour12 = 12
    elif h > 12:
        suffix = "PM"
        hour12 = h - 12

    return f"{hour12}:{m:02d} {suffix}"


def ampm_to_minutes(s):
    s = str(s).strip()
    if s.upper() == "EOD":
        return 17 * 60  # treat as 5:00 PM

    parts = s.replace(".", "").split()
    if len(parts) != 2:
        return 17 * 60

    time_part, suffix = parts[0], parts[1].upper()
    hh, mm = time_part.split(":")
    hh = int(hh)
    mm = int(mm)

    if suffix == "PM" and hh != 12:
        hh += 12
    if suffix == "AM" and hh == 12:
        hh = 0

    return hh * 60 + mm


def parse_time_input(text):
    t = str(text).strip()
    if t.upper() == "EOD":
        return 17 * 60

    parts = t.replace(".", "").split()
    if len(parts) != 2:
        return None

    time_part, suffix = parts[0], parts[1].upper()
    if suffix not in ("AM", "PM"):
        return None

    if ":" not in time_part:
        return None

    hh_str, mm_str = time_part.split(":", 1)
    if not (hh_str.isdigit() and mm_str.isdigit()):
        return None

    hh = int(hh_str)
    mm = int(mm_str)
    if hh < 1 or hh > 12 or mm < 0 or mm > 59:
        return None

    if suffix == "PM" and hh != 12:
        hh += 12
    if suffix == "AM" and hh == 12:
        hh = 0

    return hh * 60 + mm


def parse_ints(text):
    nums = []
    cur = ""
    for ch in str(text):
        if ch.isdigit():
            cur += ch
        else:
            if cur:
                nums.append(int(cur))
                cur = ""
    if cur:
        nums.append(int(cur))
    return nums


def is_truck2_only(p):
    return "truck 2" in str(getattr(p, "note", "")).lower()


def bundle_ids(packages):
    bundles = []
    seen = set()

    by_id = {p.id: p for p in packages}

    for p in packages:
        note = str(getattr(p, "note", ""))
        if "must be delivered with" in note.lower():
            ids = parse_ints(note)
            ids.append(p.id)
            group = sorted(set([i for i in ids if i in by_id]))
            key = tuple(group)
            if key not in seen and len(group) > 1:
                bundles.append(group)
                seen.add(key)

    return bundles


def assign_package(truck, p):
    truck.load(p)
    p.depart_minutes = int(round(truck.start_time))


def load_trucks(packages, t1, t2, t3):
    remaining = {p.id: p for p in packages}

    for pid in list(remaining.keys()):
        p = remaining[pid]
        if is_truck2_only(p) and len(t2.packages) < Truck.MAX_PACKAGES:
            assign_package(t2, p)
            remaining.pop(pid, None)

    bundles = bundle_ids(list(remaining.values()))
    for group in bundles:
        group_pkgs = [remaining[i] for i in group if i in remaining]
        if not group_pkgs:
            continue

        target = t1
        if any(is_truck2_only(x) for x in group_pkgs):
            target = t2

        if len(target.packages) + len(group_pkgs) <= Truck.MAX_PACKAGES:
            for p in group_pkgs:
                assign_package(target, p)
                remaining.pop(p.id, None)

    def deadline_minutes(p):
        return ampm_to_minutes(getattr(p, "deadline", "EOD"))

    early = sorted(list(remaining.values()), key=lambda p: deadline_minutes(p))

    for p in early:
        if p.id not in remaining:
            continue

        if p.id == 9:
            continue

        d = deadline_minutes(p)
        if d <= ampm_to_minutes("10:30 AM") and len(t1.packages) < Truck.MAX_PACKAGES:
            assign_package(t1, p)
            remaining.pop(p.id, None)

    for p in list(remaining.values()):
        if p.id == 9:
            continue
        if len(t2.packages) < Truck.MAX_PACKAGES:
            assign_package(t2, p)
            remaining.pop(p.id, None)

    for p in list(remaining.values()):
        if len(t3.packages) < Truck.MAX_PACKAGES:
            assign_package(t3, p)
            remaining.pop(p.id, None)


def correct_package_9(packages, now_minutes):
    if now_minutes < (10 * 60 + 20):
        return

    for p in packages:
        if p.id == 9:
            p.address = "410 S State St"
            p.city = "Salt Lake City"
            p.zip = "84111"
            return


def nearest_next_address(current_loc, packages_on_truck, dt, all_packages, now_minutes):
    correct_package_9(all_packages, now_minutes)

    best_addr = None
    best_dist = None

    for p in packages_on_truck:
        if p.id == 9 and now_minutes < (10 * 60 + 20):
            continue

        addr = p.address
        dist = dt.distance(current_loc, addr)

        if best_dist is None or dist < best_dist:
            best_dist = dist
            best_addr = addr

    return best_addr


def deliver_at_location(truck, dt, all_packages):
    here = truck.location

    for p in list(truck.packages):
        if p.address == here:
            p.mark_delivered(minutes_to_ampm(truck.time))
            p.delivered_minutes = int(round(truck.time))
            truck.packages.remove(p)


def run_route(truck, dt, all_packages):
    while truck.packages:
        next_addr = nearest_next_address(truck.location, truck.packages, dt, all_packages, truck.time)

        if next_addr is None:
            truck.time = max(truck.time, 10 * 60 + 20)
            correct_package_9(all_packages, truck.time)
            continue

        truck.drive_to(next_addr, dt)
        deliver_at_location(truck, dt, all_packages)

    truck.return_to_hub(dt)


def status_at_time(p, check_minutes):
    delivered_minutes = getattr(p, "delivered_minutes", None)
    depart_minutes = getattr(p, "depart_minutes", None)

    if delivered_minutes is not None and delivered_minutes <= check_minutes:
        return "Delivered", minutes_to_ampm(delivered_minutes)

    if depart_minutes is not None and depart_minutes <= check_minutes:
        return "En route", ""

    return "At hub", ""


def print_all_packages(packages, check_minutes):
    print(f"\n--- Package status at {minutes_to_ampm(check_minutes)} ---")
    for p in sorted(packages, key=lambda x: x.id):
        st, t = status_at_time(p, check_minutes)
        extra = f" @ {t}" if t else ""
        truck_id = getattr(p, "truck_id", "")
        truck_txt = f" (Truck {truck_id})" if truck_id else ""
        print(f"{p.id:>2}: {st}{extra}{truck_txt} - {p.address}")


def print_one_package(packages, package_id, check_minutes):
    target = None
    for p in packages:
        if p.id == package_id:
            target = p
            break

    if not target:
        print("Package not found.")
        return

    st, t = status_at_time(target, check_minutes)
    extra = f" @ {t}" if t else ""
    truck_id = getattr(target, "truck_id", "")
    truck_txt = f" (Truck {truck_id})" if truck_id else ""
    print(f"{target.id}: {st}{extra}{truck_txt}")
    print(f"Address: {target.address}, {target.city}, UT {target.zip}")
    print(f"Deadline: {target.deadline} | Weight: {target.weight} | Notes: {target.note}")


def print_truck_summary(truck):
    print(f"Truck {truck.id}:")
    print(f"Miles: {truck.miles:.1f}")
    print(f"End time: {minutes_to_ampm(truck.time)}")
    print(f"End location: {truck.location}")
    print("")


def build_and_run_simulation():
    packages = load_packages("data/packages.csv")
    dt = load_distances("data/distances.csv")

    t1 = Truck(1, start_time_minutes=8 * 60)
    t2 = Truck(2, start_time_minutes=9 * 60 + 5)
    t3 = Truck(3, start_time_minutes=10 * 60 + 20)

    load_trucks(packages, t1, t2, t3)

    run_route(t1, dt, packages)
    run_route(t2, dt, packages)

    t3.time = max(t3.time, t1.time)
    run_route(t3, dt, packages)

    total = t1.miles + t2.miles + t3.miles
    return packages, (t1, t2, t3), total


def menu(packages, trucks, total_miles):
    while True:
        print("\nWGUPS Menu")
        print("1) View ALL packages at a time")
        print("2) Look up ONE package at a time")
        print("3) View truck summary + total miles")
        print("4) Print rubric snapshots (8:45, 9:45, 12:30)")
        print("0) Exit")

        choice = input("Select: ").strip()

        if choice == "0":
            break

        if choice == "1":
            t = input("Enter time (e.g., 9:45 AM) or EOD: ").strip()
            minutes = parse_time_input(t)
            if minutes is None:
                print("Invalid time format.")
                continue
            print_all_packages(packages, minutes)

        elif choice == "2":
            pid_txt = input("Enter package ID (1-40): ").strip()
            if not pid_txt.isdigit():
                print("Invalid package ID.")
                continue
            pid = int(pid_txt)

            t = input("Enter time (e.g., 10:15 AM) or EOD: ").strip()
            minutes = parse_time_input(t)
            if minutes is None:
                print("Invalid time format.")
                continue

            print_one_package(packages, pid, minutes)

        elif choice == "3":
            print("\n--- Truck summary ---")
            for tr in trucks:
                print_truck_summary(tr)
            print(f"Total miles: {total_miles:.1f}")

        elif choice == "4":
            print_all_packages(packages, 8 * 60 + 45)
            print_all_packages(packages, 9 * 60 + 45)
            print_all_packages(packages, 12 * 60 + 30)

        else:
            print("Invalid option.")


def main():
    packages, trucks, total = build_and_run_simulation()
    print("Loaded packages:", len(packages))
    menu(packages, trucks, total)


if __name__ == "__main__":
    main()