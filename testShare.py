import unittest

from share import CSVReader, MaxFinder, FileError, MetaError, DataError


class TestCSVReader(unittest.TestCase):
    '''  
    CSVReader unit test cases
    '''
    def test_invalid_file(self):
        self.assertRaises(FileError, CSVReader, 'abc')

    def test_valid_file(self):
        csv = CSVReader('testdata/data1.csv')
        self.assertListEqual(csv.companies, ['company-a', 'company-b', 'company-c', 'company-d', 'company-e'])
        for each in csv:
            self.assertEqual(len(each), 5)
            self.assertEqual(type(each[0]), dict)
            for each_key in each[0].keys():
                self.assertIn(each_key, ['year', 'month', 'company', 'price'])

    def test_raise_meta(self):
        self.assertRaises(MetaError, CSVReader, 'testdata/data2.csv')
        self.assertRaises(MetaError, CSVReader, 'testdata/data2.csv', False)

    def test_check_skip_data_error(self):
        csv = CSVReader('testdata/data3.csv', False) # skip_data_error = False. ie donot skip err
        icsv = iter(csv)
        self.assertRaises(DataError, next, icsv)
        csv = CSVReader('testdata/data3.csv', True) # skip_data_error
        icsv = iter(csv)
        data = next(icsv)
        self.assertEqual(len(data), 5)


class TestMaxFinder(unittest.TestCase):
    '''  
    MaxFinder unit test cases
    '''
    def test_success_find(self):
        finder = MaxFinder('testdata/data1.csv', True)
        self.assertEqual(len(finder.max_values), 5)
        for each_key in finder.max_values[0].keys():
            self.assertIn(each_key, ['year', 'month', 'company', 'price'])
        self.assertEqual(finder.max_values[0]['year'], 1990)
        self.assertEqual(finder.max_values[0]['month'], 'jan')
        self.assertEqual(finder.max_values[0]['company'], 'company-a')
        self.assertEqual(finder.max_values[0]['price'], 751)


if __name__ == '__main__':
    '''  
    Run test cases: TestCSVReader & TestMaxFinder
    '''
    loader = unittest.TestLoader()
    suite1 = loader.loadTestsFromTestCase(TestCSVReader)
    suite2 = loader.loadTestsFromTestCase(TestMaxFinder)
    suite = unittest.TestSuite([suite1, suite2])

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
