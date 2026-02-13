"""
Custom hash table for packages.
Key = package ID (int)
"""

class PackageStore:
    def __init__(self, size=97):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def _hash(self, package_id):
        return package_id % self.size

    def insert(self, package_id, package):
        idx = self._hash(package_id)
        bucket = self.buckets[idx]

        for i, (k, _) in enumerate(bucket):
            if k == package_id:
                bucket[i] = (package_id, package)
                return

        bucket.append((package_id, package))

    def lookup(self, package_id):
        idx = self._hash(package_id)
        bucket = self.buckets[idx]

        for k, package in bucket:
            if k == package_id:
                return package

        return None

    def all_items(self):
        items = []
        for bucket in self.buckets:
            items.extend(bucket)
        return items