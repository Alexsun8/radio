# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

"""
[источник цифровой] -> [приёмник цифровой] -> [передатчик аналоговый] ————- [аналоговый приёмник ГРЧЦ]
"""

import abc
import json
import sys
from pydub import AudioSegment

from hashes.dejavu.dejavu import Dejavu
import hashes.dejavu.dejavu.logic.decoder as decoder

from hashes.dejavu.dejavu.config.settings import DEFAULT_FS

DEFAULT_CONFIG_FILE = "../hashes/dejavu/dejavu.cnf.SAMPLE"
filepath = "../data/test/PodShkvOgnem.mp3"


def init(configpath):
    """
    Load config from a JSON file
    """
    try:
        with open(configpath) as f:
            config = json.load(f)
    except IOError as err:
        print(f"Cannot open configuration: {str(err)}. Exiting")
        sys.exit(1)

    # create a Dejavu instance
    return Dejavu(config)


class BaseRec(object, metaclass=abc.ABCMeta):
    def __init__(self, dejavu):
        self.dejavu = dejavu
        self.Fs = DEFAULT_FS

    def rec(self, filename):
        data, self.Fs = decoder.read(filename, self.dejavu.limit)
        return self._recognize(*data)

    def _recognize(self,  *data):
        fingerprint_times = []
        # hashes = set()  # to remove possible duplicated fingerprints we built a set.
        fingerprintsArr = []

        fingerprints, fingerprint_time = self.dejavu.generate_fingerprints(data, Fs=self.Fs)
        # hashes |= set(fingerprints)

        hashesArr = [x for x, y in fingerprints]
        timeArr = [y for x, y in fingerprints]
        return hashesArr, timeArr, self.Fs

        # hashesArr = fingerprintsArr
        # hashesArr = [x for x, y in fingerprintsArr]
        # print("final res:")
        # print(hashesArr)
        # matches, dedup_hashes, query_time = self.dejavu.find_matches(hashes)

        # t = time()
        # final_results = self.dejavu.align_matches(matches, dedup_hashes, len(hashes))
        # align_time = time() - t

        # return final_results, np.sum(fingerprint_times), query_time, align_time


def hashing(songfilePath=filepath, config_file=DEFAULT_CONFIG_FILE):
    djv = init(config_file)
    baseRec = BaseRec(djv)
    return baseRec.rec(songfilePath)
