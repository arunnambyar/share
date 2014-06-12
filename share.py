import os

SKIP_DATA_ERROR = True
DATA_FILE_DIR = os.getcwd()
DATA_FILE_NAME = 'data.csv'
DATA_FILE_PATH = os.path.join(DATA_FILE_DIR, DATA_FILE_NAME)


class FileError(Exception):
    pass


class DataError(Exception):
    pass


class MetaError(Exception):
    pass


class CSVReader(object):
    SEPARATOR = ','

    def __init__(self, fpath, skip_data_err=True):
        if not os.path.exists(fpath):
            raise FileError('Invalid file name: {}'.format(fpath))
        self.fp = open(fpath)
        self.skip_data_err = skip_data_err
        self.validate = self._validate_meta_cell
        self.companies = self.raw()
        self.year, self.month = None, None
        self.validate = self._validate_data_cell

    def __iter__(self):
        return self

    def next(self):
        try:
            data = self.raw()
        except MetaError:
            print 'Error: File contains some invalid meta data'
            raise
        except DataError:
            if self.skip_data_err:
                return self.next() # skip this raw and get next raw by recursion
            raise
        else:
            return data

    def _validate_meta_cell(self, cell, index):
        if index >= 2: # Only read Company names from ["year", "month", "company1", ..]
            if not cell:
                raise MetaError('Empty meta cell found')
            return cell

    def _validate_data_cell(self, cell, index):
        if not cell:
            raise DataError('Empty data cell found')
        if index == 0: # Year value
            if not cell.isdigit():
                raise DataError('Invalid year cell {} at {} column'.format(cell, index))
            self.year = int(cell)
        elif index == 1: # Month value
            self.month = cell
        else: # Share price values one by one
            if not cell.isdigit():
                raise DataError('Invalid data cell {} at {} column'.format(cell, index))
            return {'year': self.year,
                    'month': self.month,
                    'company': self.companies[index - 2],
                    'price': int(cell)}

    def raw(self):
        index, raw_ = 0, []
        for cell in self.line().split(self.SEPARATOR):
            cell = self.validate(cell.strip().lower(), index)
            if cell is not None:
                raw_.append(cell)
            index += 1
        return raw_

    def line(self):
        line_ = self.fp.readline()
        if not line_: # empty line == '\n\r'. So empty line will not raise StopIteration
            raise StopIteration # only EOF will raise this error
        return line_.strip()


class MaxFinder(object):
    def __init__(self, fpath, skip_data_err=True):
        self.icsv = iter(CSVReader(fpath, skip_data_err)) # Company will be stored from constructor
        self.max_values = next(self.icsv) # first data line is the max value initially
        self.find_max()

    def find_max(self):
        for raw in self.icsv:
            index = 0
            for cell in raw:
                if cell['price'] >= self.max_values[index]['price']:
                    self.max_values[index] = cell
                index += 1

    def format_print(self, lines=20):
        print '*'*lines
        print 'MAX SHARE PRICE'
        print '*'*lines
        for each in self.max_values:
            print 'COMPANY :', each['company']
            print 'YEAR    :', each['year']
            print 'MONTH   :', each['month']
            print 'PRICE   :', each['price']
            print '-'*lines


if __name__ == '__main__':
    max_finder = MaxFinder(DATA_FILE_PATH, SKIP_DATA_ERROR)
    max_finder.format_print(30)
