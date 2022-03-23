"""HashTable Class"""


class HashTable:
    """Class implements a hash table using chaining method.
       HashTable dynamically grows with increased keys, but
       it does not shrink dynamically when keys are removed."""

    def __init__(self, array_size: int = 10, dictionary=None):
        if dictionary is None:
            dictionary = {}
        self.table = list()
        self.capacity = array_size

        for x in range(array_size):
            self.table.append(list())
        self.length = 0
        if dictionary is not None:
            self.update(dictionary)

    def insert(self, key, value):
        """Inserts a key, value pair into the hash table."""
        # Simple hash based on the table size
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Remove the current key value if it exists.
        self.pop(key, None)

        # Append the key, value pair to the appropriate
        # bucket list.
        bucket_list.append((key, value))
        self.length += 1

        # Resize the hash table if any bucket list is
        # larger than 10.
        if len(bucket_list) > 10:
            self.resize(self.capacity * 2)

    def __setitem__(self, key, value):
        self.insert(key, value)

    def get(self, key):
        """Returns the value associated with the key
           or raises a KeyError."""
        # Simple hash based on table size
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Scan the bucket list for key
        for item in bucket_list:
            if item[0] == key:
                return item[1]
        # Raise a KeyError is key not found
        else:
            raise KeyError

    def __getitem__(self, item):
        return self.get(item)

    def __contains__(self, item):
        try:
            value = self.get(item)
            return True
        except KeyError:
            return False

    def clear(self):
        """Delete the entire contents of the hash table."""
        for i in range(len(self.table)):
            self.table[i] = []
        self.length = 0

    def pop(self, key, *args):
        """Remove a key, value pair from the hash table
           for a given key."""
        # Scan for key and return value
        for bl in range(len(self.table)):
            for i in range(len(self.table[bl])):
                if self.table[bl][i][0] == key:
                    result = self.table[bl][i][0]
                    del self.table[bl][i]
                    self.length -= 1
                    return result
        # If key isn't found, raise KeyError or return
        # the optionally provided default value in $args
        else:
            if len(args) == 0:
                raise KeyError
            else:
                return args[0]

    def popitem(self):
        """Remove and return an item off the hash table.
           Items will be removed in no particular order."""
        return self.pop(self.keys().__next__())

    def copy(self):
        """Create and return a copy of the hash table."""
        h = HashTable()

        for (key, value) in self.items():
            h.insert(key, value)

        return h

    def items(self):
        """Return an iterator with access to the hash table
           key, value pairs."""
        return (item for bucket_list in self.table for item in bucket_list)

    def keys(self):
        """Return an iterator with access to the hash table
           keys."""
        return (x[0] for x in self.items())

    def values(self):
        """Return an iterator with access to the hash table
           values."""
        return (x[1] for x in self.items())

    def update(self, iterable):
        """Update the hash table with key, value pairs from
           the passed through iterable."""
        for (key, value) in iterable.items():
            self.insert(key, value)

    def setdefault(self, key, value=None):
        """Adds a key to the hash table and sets it's value
           to the optionally provided value only if the key
           does not already exist in the hash table.

           Returns the value associated with the key."""
        if key in self:
            return self[key]
        else:
            self.insert(key, value)
            return value

    @staticmethod
    def fromkeys(keys, value=None):
        """Creates and returns a hash table containing the
           provided keys and sets each key to the optional
           value."""
        result = HashTable()

        for key in keys:
            result.insert(key, value)

        return result

    def __len__(self):
        return self.length

    def __str__(self):
        result = '{'
        result += ", ".join([f'{key}: {value}' for (key, value) in self.items()])
        result += '}'
        return result

    def __delitem__(self, key):
        self.pop(key)

    def __iter__(self):
        return self.keys()

    def resize(self, array_size):
        """Resizes the hash table array to the provided size.
           All keys are rehashed."""
        new_hash = HashTable(array_size)

        for (key, value) in self.items():
            new_hash.insert(key, value)

        # Stealing the data from this instance
        # for the current one and chucking the rest.
        self.table = new_hash.table
        self.length = new_hash.length
        self.capacity = new_hash.capacity
