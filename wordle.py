from collections import Counter
from random import choice
import sys
from enum import Enum

from guess import *
from tile import TILE


class Helper(Enum):
    SIMPLE="simple"
    SMARTER="smarter"


class ReturnCodes(Enum):
    BAD_WORD=-1
    INCOMPLETE=0
    NEXT=1
    FINISHED=2


class Wordle:
    def __init__(self, words="data/actual_words.txt"):
        self.previous_scores = {}

        self.helper = Helper.SMARTER
        
        if len(sys.argv) > 1:
            for arg in sys.argv:
                if "-helper" in arg:
                    (_, type) = arg.split("=")
                    self.helper = Helper(type)

                if arg == "-pro":
                    words = "data/five_letter_words.txt"
        
        # print(f"Using helper: {self.helper}")

        with open(words, 'r') as file:
            self.words = file.read().split("\n")

        with open('data/cookie.txt', 'r') as file:
            f = file.read().split("\n")
            for entry in f[:-1]:
                score, number = entry.split(":")
                self.previous_scores[int(score)] = int(number)

        self.helper_options = {
            Helper.SMARTER: self.smarter_help,
            Helper.SIMPLE: self.simple_help,
        }

        self.start()

    def start(self):
        self.guesses = [[" " for _ in range(5)] for _ in range(6)]
        self.results = [[TILE.BACKGROUND for _ in range(5)] for _ in range(6)]
        self.next = [0, 0]
        self.win = False

        self.suggested_words = self.words
                
        self.target_word = choice(self.words).upper()
        # print(self.target_word)

        if self.helper == Helper.SMARTER:
            self.guess = Smarter(self.words)
            self.data = {chr(i): [] for i in range(65, 91)}
        else:
            self.guess = Simple(self.words)
            self.bad_letters = []

    def add_letter(self, letter):
        if self.next[1] < 5:
            i, j = self.next
            self.guesses[i][j] = letter
            self.next[1] = j + 1

    def enter_guess(self, benchmarking=False):
        '''
            Returns: -1: word not in list
                      0: word incomplete
                      1: next guess
                      2: game finished
        '''
        done = False
        if self.next[1] < 5 or self.next[0] == 6:
            return ReturnCodes.INCOMPLETE
        row = self.next[0]

        guess = "".join(self.guesses[row])
        if guess.lower() not in self.words:
            self.guesses[row] = [" " for _ in range(5)]
            self.next[1] = 0
            return ReturnCodes.BAD_WORD

        self.results[row] = [TILE.INCORRECT for _ in range(5)]

        found = [False for _ in range(5)]
        letters = dict(Counter(self.target_word))

        for i in range(5):
            letter = self.guesses[row][i]
            if letter == self.target_word[i]:
                found[i] = True
                self.results[row][i] = TILE.CORRECT
                letters[letter] -= 1

        for i in range(5):
            if found[i]:
                continue
            letter = self.guesses[row][i]
            if letter in self.target_word and letters[letter] > 0:
                self.results[row][i] = TILE.WRONG_PLACE
                letters[letter] -= 1
        self.next = [row + 1, 0]

        if self.results[row] == [TILE.CORRECT for _ in range(5)]:
            done = True
            self.win = True
            self.previous_scores[row + 1] += 1
        elif row == 5:
            done = True
            self.previous_scores[7] += 1
            if not benchmarking:
                print(f"The word was: {self.target_word}")
        
        if done:
            if not benchmarking:
                self.update_cookies()
            return ReturnCodes.FINISHED

        self.helper_options[self.helper](guess, row, letters)

        if not benchmarking:
            print(self.suggested_words)
            print(len(self.suggested_words))

        return ReturnCodes.NEXT

    def update_cookies(self):
        result = ""
        total_games = sum(self.previous_scores.values())
        score = 0
        for k, v in self.previous_scores.items():
            result += f"{k}:{v}\n"
            score += k * v
        
        with open("data/cookie.txt", "w") as f:
            f.write(result)

        print(f"Average score is: {score/total_games}")

    def simple_help(self, guess, row, letters):
        for (l, r) in zip(guess, self.results[row]):
            if r == TILE.INCORRECT and l not in letters.keys():
                self.bad_letters.append(l)
        self.suggested_words = self.guess.guess(guess, self.results[row], self.bad_letters)

    def smarter_help(self, guess, row, letters):
        for (i, (l, r)) in enumerate(zip(guess, self.results[row])):
            if (r, i) not in self.data[l]:
                if r == TILE.INCORRECT and len(self.data[l]) != 0:
                    continue
                self.data[l].append((r, i))

        self.suggested_words = self.guess.guess(guess, self.data)


def main():
    pass


if __name__ == "__main__":
    main()
