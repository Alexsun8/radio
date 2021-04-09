import unittest
from calculatePrRec import iterate
from pathlib import Path
import csv


class MyTestCase(unittest.TestCase):
    def test_prRecPoint(self):
        dataDir = Path('/home/alexsun8/streamlabs/radio/data/Список радио сравнения трансляций')
        resFile = Path('/home/alexsun8/streamlabs/radio/data/PrRes.txt')

        testDict = iterate(dataDir, True)
        num_of_good = 0
        total = 0
        print('here')
        with open('./data/answers.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                print(row)
                fileStem = Path(row[1]).stem
                if row[2] != '!!!!':
                    time = '.'.join(row[2].split(':'))
                    if abs(int(time) - testDict[fileStem])<= 5:
                        print('True')
                        num_of_good+=1
                    else:
                        print('False')
                    total+=1

        print(f'right: {num_of_good}; total: {total}')
        self.assertGreater(0.5, num_of_good/total)


if __name__ == '__main__':
    unittest.main()
