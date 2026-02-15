# Simple hash table for packages using separate chaining
# Key: package_id (int) - Value: package object

class PackageStore:
    def __init__(self, size=97):
        self.size = size
        
        # Each bucket is a list of (key, value) pairs (separate chaining)
        self.buckets = [[] for _ in range(size)] 

    def _hash(self, package_id):
        # Map the package ID to a bucket index
        return package_id % self.size

    def insert(self, package_id, package):
        # Insert a new (id, package) pair, or overwrite it if the ID already exists
        idx = self._hash(package_id)
        bucket = self.buckets[idx]

        for i, (k, _) in enumerate(bucket):
            if k == package_id:
                bucket[i] = (package_id, package)
                return

        bucket.append((package_id, package))

    def lookup(self, package_id):
        # Return the package object for this ID, or None if not found
        idx = self._hash(package_id)
        bucket = self.buckets[idx]

        for k, package in bucket:
            if k == package_id:
                return package

        return None

    def all_items(self):
        # Flatten for iteration/reporting
        items = []
        for bucket in self.buckets:
            items.extend(bucket)
        return items