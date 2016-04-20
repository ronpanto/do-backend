
from storage.MemStorage import MemStorage
import logging
logger = logging.getLogger('server')

class BusinessLogic(object):
    """
        Business logic is static, we don't really instanciate it, but call just call its functions.
        It handles the protocol parsing and compliance and does high-level logic for each action
    """
    # This chooses which storage layer to use
    STORAGE_LAYER = MemStorage()
    QUERY_VERB = "QUERY"
    INDEX_VERB = "INDEX"
    REMOVE_VERB = "REMOVE"

    POSSIBLE_VERBS = set([QUERY_VERB, INDEX_VERB, REMOVE_VERB])

    @classmethod
    def handle_message(cls, message_buffer):
        """
        This is our protocol function. It get a line that was received on a socket, parses it, activates the right logic
        and then sends the proper respond back to the wire
        :param message_buffer: the buffer as received from the socket
        :return: the response to be sent to the client
        """
        # We split by "|" to get the verb|package_name|<dependencies>
        buffer_parts = message_buffer.split("|")
        try:
            # Enforcing that indeed there were two '|' signs (meaning that all parts were there)
            if len(buffer_parts) != 3:
                raise Exception("Protocol Error")
            verb, package_name, deps_str = buffer_parts
            if deps_str == "":
                deps = []
            else:
                # If the client sent dependencies, we split them by ','
                deps = deps_str.split(",")

            if verb not in cls.POSSIBLE_VERBS:
                raise Exception("Unknown verb")
            if not package_name:
                raise Exception("Package name is empty")

            if verb == cls.QUERY_VERB:
                result = cls.query(package_name)
            elif verb == cls.INDEX_VERB:
                result = cls.index(package_name, deps)
            elif verb == cls.REMOVE_VERB:
                result = cls.remove(package_name)
            else:
                pass

            if result:
                return "OK\n"
            else:
                return "FAIL\n"

        except Exception, ex:
            logger.exception("error %s" % buffer)
            return "ERROR\n"

    @classmethod
    def query(cls, package):
        """

        :param package: package name
        :return: True if the package exists in the storage, False otherwise
        """
        return not cls.STORAGE_LAYER.get_entry(package) is False

    @classmethod
    def index(cls, package, deps=[]):
        """
        Indexing a package
        :param package: package name
        :param deps: collection of dependencies as strings
        :return: True if package already exists or if it can be indexed(dependencies exist) - False otherwise
        """
        # If the package already exists, we can just return True
        if cls.STORAGE_LAYER.get_entry(package) is not False:
            return True
        else:
            # If the package does not exist, we have to check that all dependencies are indexed, and only then add it
            if cls.STORAGE_LAYER.check_many_exist(deps):
                cls.STORAGE_LAYER.add_entry(package, deps)
                return True
            else:
                logger.error("FAILED INDEX %s %s" % (package, deps))
                return False

    @classmethod
    def remove(cls, package):
        """

        :param package: package name
        :return: True if package does not exist, or if packaged can be removes (Nothing depends on it), else False
        """
        if cls.STORAGE_LAYER.get_entry(package) is False:
            return True
        else:
            if cls.STORAGE_LAYER.check_dependents(package):
                return False

            cls.STORAGE_LAYER.remove_entry(package)
            return True
