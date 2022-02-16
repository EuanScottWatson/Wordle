from tile import TILE


class Simple:
    def __init__(self, world_list):
        self.word_list = world_list

    def update_world_list(self, world_list):
        self.word_list = world_list

    def guess(self, guess, results, bad_letters=[]):
        new_words = []
        for w in self.word_list:
            if w == guess:
                continue
            word = w.upper()
            good = True
            for i, result in enumerate(results):
                if result == TILE.CORRECT and word[i] != guess[i]:
                    good = False

                if result == TILE.WRONG_PLACE and guess[i] not in word:
                    good = False

                if word[i] in bad_letters:
                    good = False
            
            if good:
                new_words.append(word)
        
        self.update_world_list(new_words)
        return new_words


class Smarter:
    def __init__(self, world_list):
        self.word_list = world_list

    def update_world_list(self, world_list):
        self.word_list = world_list

    def guess(self, guess, data):
        # data = {LETTER: [TILE, POSITION]}
        new_words = []
        for w in self.word_list:
            word = w.upper()
            if word == guess:
                continue
            good = True
            for (k, v) in data.items():
                for (t, p) in v:
                    if t == TILE.INCORRECT and k in word:
                        good = False
                    
                    if t == TILE.WRONG_PLACE and (word[p] == k or k not in word):
                        good = False
                    
                    if t == TILE.CORRECT and word[p] != k:
                        good = False

            if good:
                new_words.append(word)

        self.update_world_list(new_words)
        return new_words



def main():
    words = []
    with open("data/actual_words.txt", 'r') as file:
            words = file.read().split("\n")
    
    guess = "HELLO"
    results = [TILE.WRONG_PLACE, TILE.INCORRECT, TILE.CORRECT, TILE.CORRECT, TILE.INCORRECT]
    bad_letters = ["S", "N", "I", "R", "Y", "D", "T"]
    data = {'A': [((83, 141, 78), 2)], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [((58, 58, 58), 3)], 'J': [], 'K': [], 'L': [((181, 159, 59), 4)], 'M': [], 'N': [((58, 58, 58), 1)], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [((181, 159, 59), 0)], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}

    # words = ['ABLED', 'ADULT', 'AFOUL', 'AGLOW', 'ALBUM', 'ALGAE', 'ALLOT', 'ALLOW', 'ALOFT', 'ALOOF', 'ALOUD', 'ALPHA', 'AMBLE', 'AMPLE', 'APPLE', 'ATOLL', 'AWFUL', 'BAGEL', 'BLACK', 'BLADE', 'BLAME', 'BLAZE', 'BLEAK', 'BLEAT', 'BLOAT', 'CABAL', 'CABLE', 'CAMEL', 'CAULK', 'CHALK', 'CLACK', 'CLAMP', 'CLEAT', 'CLOAK', 'DEALT', 'DECAL', 'DELTA', 'EAGLE', 'ECLAT', 'ELATE', 'EQUAL', 'EXALT', 'FABLE', 'FATAL', 'FAULT', 'FECAL', 'FELLA', 'FETAL', 'FLACK', 'FLAKE', 'FLAME', 'FLOAT', 'FOCAL', 'GAVEL', 'GLADE', 'GLAZE', 'GLEAM', 'GLOAT', 'HALVE', 'HAZEL', 'KOALA', 'LABEL', 'LADLE', 'LAPEL', 'LATCH', 'LATHE', 'LATTE', 'LAUGH', 'LEACH', 'LEAPT', 'LEAVE', 'LEGAL', 'LLAMA', 'LOATH', 'LOCAL', 'MAPLE', 'MEDAL', 'METAL', 'MODAL', 'OCTAL', 'OFFAL', 'PAPAL', 'PEDAL', 'PETAL', 'PLACE', 'PLATE', 'PLAZA', 'PLEAD', 'PLEAT', 'POLKA', 'PUPAL', 'QUALM', 'TABLE', 'TOTAL', 'TUBAL', 'VALET', 'VALUE', 'VALVE', 'VAULT', 'VOCAL', 'WALTZ', 'WHALE']
    words = ['BUYER', 'ABLED', 'LEAST']
    g = Smarter(world_list=words)
    print(g.guess(guess, data))

if __name__ == "__main__":
    main()