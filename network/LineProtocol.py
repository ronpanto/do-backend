import logging
logger = logging.getLogger("server")

class LineProtocol(object):
    QUERY_VERB = "QUERY"
    INDEX_VERB = "INDEX"
    REMOVE_VERB = "REMOVE"

    POSSIBLE_VERBS = set([QUERY_VERB, INDEX_VERB, REMOVE_VERB])

    def __init__(self, business_logic):
        self.business_logic = business_logic


    def handle_message(self, message_buffer):
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
                if not all(deps):
                    raise Exception("Empty Dependencies found")

            if verb not in self.POSSIBLE_VERBS:
                raise Exception("Unknown verb")
            if not package_name:
                raise Exception("Package name is empty")

            if verb == self.QUERY_VERB:
                result = self.business_logic.query(package_name)
            elif verb == self.INDEX_VERB:
                result = self.business_logic.index(package_name, deps)
            elif verb == self.REMOVE_VERB:
                result = self.business_logic.remove(package_name)
            else:
                pass

            if result:
                return "OK\n"
            else:
                return "FAIL\n"

        except Exception, ex:
            logger.exception("error %s" % buffer)
            return "ERROR\n"