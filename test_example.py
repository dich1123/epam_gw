import unittest


def good_name(name, surname):
    return f'{name.upper()} {surname.upper()}'


class TestNames(unittest.TestCase):
    def test_good_name(self):
        answ = good_name('dima', 'cherenkov')
        print('test_example_run')
        self.assertEqual(answ, 'DIMA CHERENKOV')


if __name__ == '__main__':
    unittest.main()