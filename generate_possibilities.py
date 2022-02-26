from itertools import product
from math import comb
import math
import matplotlib.pyplot as plt
import threading
import sys

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

        # Get all the 3^5 combinations
        self.combinations = list(map(lambda x: self.num_to_tile(x), product(range(3), repeat=5)))

    # Takes in a tuple of 5 numbers, returning the TILE format of the result
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
        # For every word, check every combination and generate the information gained from this
        for i, word in enumerate(self.words):
            word = word.upper()
            probabilities = []
            for comb in self.combinations:
                data = {word[i]: [(comb[i], i)] for i in range(5)}

                words = self.smart.guess(word, data, update=False)
                probabilities.append(len(words) / self.total_words)
            
            # Sort the probabilities of each combination
            probabilities.sort(reverse=True)
            information = round(sum((x * math.log2(1 / x)) for x in filter(lambda x: x != 0, probabilities)), 2)
            printProgressBar(i + 1, len(self.words), suffix=f"{word} = {information} bits")
            word_information.append((word, information))

            # Update the relevant text file with the newest information calculated
            with open(f'information/uniform_information_thread_{self.thread}.txt', 'w') as fp:
                fp.write('\n'.join('%s, %s' % x for x in word_information))


def threads(total_words, words, thread, all_words):
    g = Generator(total_words=total_words, words=words, thread=thread, all_words=all_words)
    g.generate()


def main():
    # All ~13,000 words
    with open("data/five_letter_words.txt", 'r') as file:
        words = file.read().split("\n")

    # Get the number of threads and how many words each thread will deal with
    total_words = len(words)
    total_threads = 4
    for arg in sys.argv:
        if "-threads" in arg:
            _, t = arg.split("=")
            total_threads = int(t)
    
    slices = total_words // total_threads

    # Start all threads
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

    # Collect all the data created and merge back into one large file
    all_information = []
    for i in range(total_threads):
        file = f"information/uniform_information_thread_{i}.txt"
        with open(file, 'r') as f:
            all_information.extend(f.read().split("\n"))
    
    with open(f'information/uniform_information.txt', 'w') as fp:
        fp.write('\n'.join(x for x in all_information))



if __name__ == "__main__":
    main()