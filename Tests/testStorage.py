import unittest

from storage.MemStorage import MemStorage
class MemStorageTests(unittest.TestCase):

    def setUp(self):
        self.storage = MemStorage()

    def testOne(self):
        self.basic_add_get_remove(1)

    def testStress(self):
        self.basic_add_get_remove(5000)



    def basic_add_get_remove(self, num_packages=1):
        for i in xrange(num_packages):
            # Adding the last 20 packages as dependencies
            self.storage.add_entry("package%s" % i, ["package%s" % k for k in xrange(max(i-20,0) , i)])

        for i in xrange(num_packages):
            result = self.storage.get_entry("package%s" % i)
            self.assertEqual(result, ["package%s" % k for k in xrange(max(i-20,0) , i)])

        for i in xrange(num_packages-1, -1,  -1):
            self.storage.remove_entry("package%s" % i)

        for i in xrange(num_packages):
            result = self.storage.get_entry("package%s" % i)
            self.assertEqual(result, False)


