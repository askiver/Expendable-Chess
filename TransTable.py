import random
import time

import numpy as np


class TransTable:
    def __init__(self):
        random.seed(time.time())

        self.hash_table = np.zeros(shape=(2,6,64), dtype=np.int32)
        self.hash_side = self.random_hash()
        self.hash_ep = np.zeros(64, dtype=np.int32)

        for i in range(2):
            for j in range(6):
                for k in range(64):
                    self.hash_table[i][j][k] = self.random_hash()
        for i in range(64):
            self.hash_ep[i] = self.random_hash()


    def random_hash(self):
        return random.getrandbits(32)

    def hash(self, side:int, pieces:np.ndarray, colour:np.ndarray, ep:int):
        hash_value = 0
        for i in range(64):
            if colour[i] != 6:
                hash_value = np.bitwise_xor(hash_value, self.hash_table[colour[i]][pieces[i]][i])
        if side:
            hash_value = np.bitwise_xor(hash_value, self.hash_side)
        if ep != -1:
            hash_value = np.bitwise_xor(hash_value, self.hash_ep[ep])
        return hash_value


