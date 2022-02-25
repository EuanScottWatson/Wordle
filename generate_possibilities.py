from itertools import product
from math import comb
import math
from turtle import pos
import matplotlib.pyplot as plt

from guess import Smarter
from tile import TILE

class Generator:
    def __init__(self, word, words="data/actual_words.txt") -> None:
        self.word = word.upper()
        with open(words, 'r') as file:
            self.words = file.read().split("\n")

        self.smart = Smarter(self.words)

        self.combinations = list(map(lambda x: self.num_to_tile(x), product(range(3), repeat=5)))
        self.xticks = ["".join([str(c) for c in comb]) for comb in product(range(3), repeat=5)]

    def num_to_tile(self, tuple):
        res = []
        for result in tuple:
            if result == 0:
                res.append(TILE.INCORRECT)
            elif result == 1:
                res.append(TILE.WRONG_PLACE)
            else:
                res.append(TILE.CORRECT)
        return res

    def generate(self):
        total_words = len(self.words)
        probabilities = []
        for comb in self.combinations:
            data = {self.word[i]: [(comb[i], i)] for i in range(5)}

            words = self.smart.guess(self.word, data, update=False)
            probabilities.append(len(words) / total_words)
        
        probabilities.sort(reverse=True)
        information = round(sum((x * math.log2(1 / x)) for x in filter(lambda x: x != 0, probabilities)), 2)
        print(f"The information gained from {self.word} was {information} bits")

        # plt.plot(probabilities)
        # plt.show()


def main():
    g = Generator("TARES", words="data/five_letter_words.txt")
    g.generate()


if __name__ == "__main__":
    main()