
from storage.MemStorage import MemStorage
import logging
logger = logging.getLogger('server')

class BusinessLogic(object):
    """
        It handles the protocol parsing and compliance and does high-level logic for each action
    """

    def __init__(self, storage_layer):
        self.storage_layer = storage_layer

    def query(self, package):
        """

        :param package: package name
        :return: True if the package exists in the storage, False otherwise
        """
        return not self.storage_layer.get_entry(package) is False

    def index(self, package, deps=[]):
        """
        Indexing a package
        :param package: package name
        :param deps: collection of dependencies as strings
        :return: True if package already exists or if it can be indexed(dependencies exist) - False otherwise
        """
        # If the package already exists, we can just return True
        if self.storage_layer.get_entry(package) is not False:
            return True
        else:
            # If the package does not exist, we have to check that all dependencies are indexed, and only then add it
            if self.storage_layer.check_many_exist(deps):
                self.storage_layer.add_entry(package, deps)
                return True
            else:
                logger.error("FAILED INDEX %s %s" % (package, deps))
                return False

    def remove(self, package):
        """

        :param package: package name
        :return: True if package does not exist, or if packaged can be removes (Nothing depends on it), else False
        """
        if self.storage_layer.get_entry(package) is False:
            return True
        else:
            if self.storage_layer.check_dependents(package):
                return False

            self.storage_layer.remove_entry(package)
            return True
