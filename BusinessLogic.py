
from storage.MemStorage import MemStorage

class BusinessLogic(object):
    STORAGE_LAYER = MemStorage

    POSSIBLE_VERBS = set(["QUERY", "INDEX", "REMOVE"])

    @classmethod
    def handle_message(cls, buffer):
            print "handling %s" % buffer
            buffer_parts = buffer.split("|")
            try:
                if len(buffer_parts) != 3:
                    raise Exception("Syntax Error")
                verb, package_name, deps = buffer_parts
                if not verb in cls.POSSIBLE_VERBS:
                    raise Exception("Unknown verb")
                if not package_name:
                    raise Exception("Package name is empty")
                return "OK\n"
            except Exception, ex:
                return "ERROR\n"

    def query(self, package):
        pass

    def index(self, package, deps=[]):
        pass

    def remove(self, package):
        pass
