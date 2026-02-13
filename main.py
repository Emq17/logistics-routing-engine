# Student ID: 010306042

from hash_table import PackageStore

store = PackageStore()
store.insert(1, {"name": "Test Package 1"})
store.insert(2, {"name": "Test Package 2"})

print(store.lookup(1))
print(store.lookup(2))
print(store.lookup(3))