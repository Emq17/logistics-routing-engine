# Student ID: 010306042

from hash_table import PackageStore
from loader import load_packages, load_distances


def main():
    store = PackageStore()
    packages = load_packages("data/packages.csv")

    for p in packages:
        store.insert(p.package_id, p)

    dt = load_distances("data/distances.csv")

    print("Loaded packages:", len(packages))
    print("Distance HUB -> 195 W Oakland Ave:", dt.distance("HUB", "195 W Oakland Ave"))
    print("Distance 300 State St -> 195 W Oakland Ave:", dt.distance("300 State St", "195 W Oakland Ave"))


if __name__ == "__main__":
    main()