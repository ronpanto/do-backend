from BusinessLogic import BusinessLogic
from storage.MemStorage import MemStorage
import unittest
class BLTests(unittest.TestCase):

    def setUp(self):
        self.bl = BusinessLogic(storage_layer=MemStorage())

    def testRemoveNonExist(self):
        response = self.bl.remove("package")
        self.assertEqual(response, True)
        for i in xrange(200):
            self.bl.index("p%s" % i)
        response = self.bl.remove("package")
        self.assertEqual(response, True)

    def testRemoveExisting(self):
        num_packages = 200
        for i in xrange(num_packages):
            self.bl.index("p%s" % i)
        for i in xrange(num_packages):
            response = self.bl.remove("p%s")
            self.assertEqual(response, True)

    def testRemoveWithDeps(self):
        self.bl.index("p1")
        self.bl.index("p2", ["p1"])
        response = self.bl.remove("p1")
        self.assertEqual(response, False)

    def testIndex(self):
        self.bl.index("p1")
        response = self.bl.query("p1")
        self.assertNotEqual(response, False)

    def testIndexExists(self):
        self.bl.index("p1")
        response = self.bl.query("p1")
        self.assertNotEqual(response, False)
        self.bl.index("p1")
        self.assertEqual(response, True)

    def testIndexDepsDoesNotExist(self):
        response = self.bl.index("p5", ["p4"])
        self.assertEqual(response, False)

    def queryNonExist(self):
        response = self.bl.query("p1000")
        self.assertEqual(response, False)