from itertools import product
from math import comb
import math
import matplotlib.pyplot as plt
import threading

from guess import Smarter
from tile import TILE
from benchmark import printProgressBar

class Generator:
    def __init__(self, total_words, words, thread, all_words):
        self.thread = thread
        self.total_words = total_words
        self.words = words
        self.all_words = all_words

        self.smart = Smarter(self.all_words)

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
        word_information = []
        for i, word in enumerate(self.words):
            word = word.upper()
            probabilities = []
            for comb in self.combinations:
                data = {word[i]: [(comb[i], i)] for i in range(5)}

                words = self.smart.guess(word, data, update=False)
                probabilities.append(len(words) / self.total_words)
            
            probabilities.sort(reverse=True)
            information = round(sum((x * math.log2(1 / x)) for x in filter(lambda x: x != 0, probabilities)), 2)
            printProgressBar(i + 1, len(self.words), suffix=f"{word} = {information} bits")
            word_information.append((word, information))

            with open(f'information/uniform_information_thread_{self.thread}.txt', 'w') as fp:
                fp.write('\n'.join('%s, %s' % x for x in word_information))


def threads(total_words, words, thread, all_words):
    g = Generator(total_words=total_words, words=words, thread=thread, all_words=all_words)
    g.generate()


def main():
    with open("data/five_letter_words.txt", 'r') as file:
        words = file.read().split("\n")

    total_words = len(words)
    total_threads = 4
    slices = total_words // total_threads

    ts = []
    for i in range(total_threads):
        subset_words = words[i * slices: (i+1) * slices]

        x = threading.Thread(target=threads, args=(total_words, subset_words, i, words,))
        ts.append(x)
        print(f"Starting thread {i}")
        x.start()

    for t in ts:
        t.join()
        print(f"Thread {ts.index(t) + 1} finished")

    all_information = []
    for i in range(total_threads):
        file = f"information/uniform_information_thread_{i}.txt"
        with open(file, 'r') as f:
            all_information.extend(f.read().split("\n"))
    
    with open(f'information/uniform_information.txt', 'w') as fp:
        fp.write('\n'.join(x for x in all_information))



if __name__ == "__main__":
    main()