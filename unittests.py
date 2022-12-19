import unittest
import spark

class SparkTests(unittest.TestCase):
    def test_parse_int(self):
        self.assertEqual(1, spark.parse(1))
        self.assertEqual(23, spark.parse(23))
        self.assertEqual(100, spark.parse(100))
        self.assertEqual(4000000, spark.parse(4000000))


if __name__ == "__main__":
    unittest.main()