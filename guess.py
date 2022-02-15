from tile import TILE


class Guess:
    def __init__(self, world_list):
        self.word_list = world_list

    def update_world_list(self, world_list):
        self.word_list = world_list

    def data(self, guess, results):
        new_words = []
        for w in self.word_list:
            word = w.upper()
            good = True
            for i, result in enumerate(results):
                if result == TILE.CORRECT and word[i] != guess[i]:
                    good = False

                if result == TILE.WRONG_PLACE and guess[i] not in word:
                    good = False
            
            if good:
                new_words.append(word)
        
        return new_words


def main():
    words = []
    with open("data/actual_words.txt", 'r') as file:
            words = file.read().split("\n")
    
    guess = "DEBBY"
    results = [TILE.CORRECT, TILE.CORRECT, TILE.WRONG_PLACE, TILE.INCORRECT, TILE.INCORRECT]

    g = Guess(world_list=words)
    print(g.data(guess, results))

if __name__ == "__main__":
    main()