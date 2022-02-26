import pygame, os
from pygame.locals import *
import sys

from wordle import *
from tile import TILE


class WordleGUI:
    # Produces a screen to play Wordle
    def __init__(self):
        self.brain = Wordle()
        self.timer = 0
        self.done = False

        self.guess = "-guess" in sys.argv

    def display(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 60)
        for i in range(6):
            for j in range(5):
                rect = pygame.Rect(30 + 110 * j, 25 + 110 * i, 100, 100)
                pygame.draw.rect(screen, self.brain.results[i][j], rect, 0, 2)
                if self.brain.results[i][j] == TILE.BACKGROUND:
                    pygame.draw.rect(screen, TILE.INCORRECT, rect, 2, 2)

                guess = font.render(self.brain.guesses[i][j], True, (255, 255, 255))
                gues_rect = guess.get_rect(center=(30 + 110 * j + 50, 25 + 110 * i + 55))
                screen.blit(guess, gues_rect)
        
        if self.done or self.timer > 0:
            text = "Well Done!" if self.brain.win else ("Not a word" if self.timer > 0 else "Unlucky")
            guess = font.render(text, True, (255, 255, 255))
            gues_rect = guess.get_rect(center=(300, 740))
            screen.blit(guess, gues_rect)
            self.timer -= 1

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key in range(97, 123) and not self.done:
                    self.brain.add_letter(chr(event.key - 32))
                if event.key in range(48, 51) and self.brain.row_typed() and self.guess:
                    self.brain.add_result(int(chr(event.key)))
                if event.key == K_BACKSPACE and not self.done:
                    if self.brain.next[1] > 0 and self.brain.next_result[1] == 0:
                        i, j = self.brain.next
                        self.brain.guesses[i][j - 1] = " "
                        self.brain.next[1] = j - 1
                    if self.brain.next_result[1] > 0:
                        i, j = self.brain.next_result
                        self.brain.results[i][j - 1] = TILE.BACKGROUND
                        self.brain.next_result[1] = j - 1
                if event.key == K_RETURN:
                    self.enter_guess()
                if event.key == K_ESCAPE:
                    return True
                if event.key == K_TAB:
                    self.done = False
                    self.brain.start()

    def display_screen(self, screen):
        screen.fill((18, 18, 19))

        self.display(screen)

        pygame.display.update()
        pygame.display.flip()

    def enter_guess(self):
        returnValue = self.brain.enter_guess(user_guessing=self.guess)
        if returnValue == ReturnCodes.FINISHED:
            self.done = True
        elif returnValue == ReturnCodes.BAD_WORD:
            self.timer = 60


def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("WordleGUI")

    os.environ['SDL_VIDEO_CENTERED'] = "True"

    width, height = 600, 800

    screen = pygame.display.set_mode((width, height))

    done = False
    clock = pygame.time.Clock()
    wordleGUI = WordleGUI()

    while not done:
        done = wordleGUI.events()
        wordleGUI.display_screen(screen)

        clock.tick(60)


if __name__ == "__main__":
    main()
