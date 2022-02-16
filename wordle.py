import pygame, os
from pygame.locals import *
from collections import Counter
from random import choice
import sys
from enum import Enum

from guess import *
from tile import TILE


class Helper(Enum):
    SIMPLE="simple"
    SMARTER="smarter"


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
        
        print(f"Using helper: {self.helper}")

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
        self.done = False
        self.win = False
        self.timer = 0
                
        self.target_word = choice(self.words).upper()
        # print(self.target_word)

        if self.helper == Helper.SMARTER:
            self.guess = Smarter(self.words)
            self.data = {chr(i): [] for i in range(65, 91)}
        else:
            self.guess = Simple(self.words)
            self.bad_letters = []

    def display(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 60)
        for i in range(6):
            for j in range(5):
                rect = pygame.Rect(30 + 110 * j, 25 + 110 * i, 100, 100)
                pygame.draw.rect(screen, self.results[i][j], rect, 0, 2)
                if self.results[i][j] == TILE.BACKGROUND:
                    pygame.draw.rect(screen, TILE.INCORRECT, rect, 2, 2)

                guess = font.render(self.guesses[i][j], True, (255, 255, 255))
                gues_rect = guess.get_rect(center=(30 + 110 * j + 50, 25 + 110 * i + 55))
                screen.blit(guess, gues_rect)
        
        if self.done or self.timer > 0:
            text = "Well Done!" if self.win else ("Not a word" if self.timer > 0 else "Unlucky")
            guess = font.render(text, True, (255, 255, 255))
            gues_rect = guess.get_rect(center=(300, 740))
            screen.blit(guess, gues_rect)
            self.timer -= 1

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key in range(97, 123):
                    if self.next[1] < 5 and not self.done:
                        i, j = self.next
                        self.guesses[i][j] = chr(event.key - 32)
                        self.next[1] = j + 1
                if event.key == K_BACKSPACE:
                    if self.next[1] > 0:
                        i, j = self.next
                        self.guesses[i][j - 1] = " "
                        self.next[1] = j - 1
                if event.key == K_RETURN:
                    self.enter_guess()
                if event.key == K_ESCAPE:
                    return True
                if event.key == K_TAB:
                    self.start()

    def display_screen(self, screen):
        screen.fill((18, 18, 19))

        self.display(screen)

        pygame.display.update()
        pygame.display.flip()

    def enter_guess(self):
        if self.next[1] < 5 or self.next[0] == 6:
            return
        row = self.next[0]

        guess = "".join(self.guesses[row])
        if guess.lower() not in self.words:
            self.guesses[row] = [" " for _ in range(5)]
            self.next[1] = 0
            self.timer = 60
            return

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
            self.done = True
            self.win = True
            self.previous_scores[row + 1] += 1
        elif row == 5:
            self.done = True
            self.previous_scores[7] += 1
            print(f"The word was: {self.target_word}")
        
        if self.done:
            self.update_cookies()
            return

        self.helper_options[self.helper](guess, row, letters)

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
        possible_words = self.guess.guess(guess, self.results[row], self.bad_letters)
        print(possible_words)
        print(len(possible_words))

    def smarter_help(self, guess, row, letters):
        print("Smart")
        for (i, (l, r)) in enumerate(zip(guess, self.results[row])):
            if (r, i) not in self.data[l]:
                if r == TILE.INCORRECT and len(self.data[l]) != 0:
                    continue
                self.data[l].append((r, i))

        possible_words = self.guess.guess(self.data)
        print(possible_words)
        print(len(possible_words))



def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Wordle")

    os.environ['SDL_VIDEO_CENTERED'] = "True"

    width, height = 600, 800

    screen = pygame.display.set_mode((width, height))

    done = False
    clock = pygame.time.Clock()
    wordle = Wordle()

    while not done:
        done = wordle.events()
        wordle.display_screen(screen)

        clock.tick(60)


if __name__ == "__main__":
    main()
