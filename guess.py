from tile import TILE


class Simple:
    # A simple helper which only takes in incorrect letters and doesn't regard wrongly placed letters
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

    def guess(self, guess, data, update=True):
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

        if update:
            self.update_world_list(new_words)
        return new_words


def main():
    pass

if __name__ == "__main__":
    main()