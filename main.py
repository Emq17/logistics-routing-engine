# Student ID: 010306042

from hash_table import PackageStore
from package import Package

def main():
    store = PackageStore()

    p = Package(1, "123 Test St", "Test City", "00000", "EOD", 5)
    store.insert(1, p)

    print(store.lookup(1))

if __name__ == "__main__":
    main()