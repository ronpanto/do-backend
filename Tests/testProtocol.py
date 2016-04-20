from BusinessLogic import BusinessLogic
from network.LineProtocol import LineProtocol
import unittest

from storage.MemStorage import MemStorage
class ProtocolTests(unittest.TestCase):

    def setUp(self):
        self.protocol_handler = LineProtocol(BusinessLogic(storage_layer=MemStorage()))

    def testBadVerbs(self):
        response = self.protocol_handler.handle_message("TEST|package|")
        self.assertEqual(response, "ERROR\n")
        response = self.protocol_handler.handle_message("VERB|package|")
        self.assertEqual(response, "ERROR\n")
        response = self.protocol_handler.handle_message("BAD|package|")
        self.assertEqual(response, "ERROR\n")

    def testVerbs(self):
        response = self.protocol_handler.handle_message("INDEX|package|")
        self.assertEqual(response, "OK\n")
        response = self.protocol_handler.handle_message("QUERY|package|")
        self.assertEqual(response, "OK\n")
        response = self.protocol_handler.handle_message("REMOVE|package|")
        self.assertEqual(response, "OK\n")


    def testSyntaxErrors(self):
        for verb in LineProtocol.POSSIBLE_VERBS:
            response = self.protocol_handler.handle_message("%s|package" % verb)
            self.assertEqual(response, "ERROR\n")
        response = self.protocol_handler.handle_message("INDEX||dep1,dep2")
        self.assertEqual(response, "ERROR\n")
        response = self.protocol_handler.handle_message("INDEX|package|,,,,")
        self.assertEqual(response, "ERROR\n")
