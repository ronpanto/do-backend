from GenericStorage import GenericStorage
import threading
from collections import defaultdict
class MemStorage(GenericStorage):
    """
        This class implements the GenericStorage interface, with an underlying in-mem dictionary object
        as the storage
    """

    def __init__(self):
        """
            self.storage - dictionary from package name to list of dependencies
            self.deps_storage - dictionary from a package name to a set of packages that depend on it
            self.write_lock - a locking object for our multithreaded environment

        """
        self.storage = dict()
        self.deps_storage = defaultdict(set)
        self.write_lock = threading.RLock()

    def add_entry(self, package, deps):
        """
        In order to add a package, we have to add it to the storage dict (and the deps list as the value)
        plus, we have to add it as a dependent for each of its dependencies in the deps_storage dictionary
        """
        self.write_lock.acquire()
        self.storage[package] = deps
        for dep in deps:
            self.deps_storage[dep].add(package)

        self.write_lock.release()

    def remove_entry(self, package):

        self.write_lock.acquire()
        # Phase 1 - remove this package from the dependents set of each of the packages that depend on it
        for dep in self.storage[package]:
            self.deps_storage[dep].remove(package)
        # Phase 2 - remove this package from the list of indexed packages
        del self.storage[package]
        # Phase 3- remove the package from deps_storage , which means that now nothing depends on it
        if package in self.deps_storage:
            del self.deps_storage[package]
        self.write_lock.release()

    def get_entry(self, package):
        self.write_lock.acquire()
        # Just retrieving the list of dependencies, False if it is not in the storage
        result = self.storage.get(package, False)
        self.write_lock.release()
        return result

    def check_many_exist(self, packages):
        self.write_lock.acquire()
        result = True
        for package in packages:
            if package not in self.storage:
                result = False
                break
        self.write_lock.release()
        return result

    def check_dependents(self, package):
        self.write_lock.acquire()
        result = bool(self.deps_storage.get(package, None))
        self.write_lock.release()
        return result
