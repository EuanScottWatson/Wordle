from random import choice

from wordle import *

def main():
    wordle = Wordle()
    average = 0
    total = 1000
    for _ in range(total):
        # start = choice(wordle.words).upper()
        start = "SNAIL"
        word = start
        done = ReturnCodes.NEXT
        guesses = 0
        while done == ReturnCodes.NEXT:
            guesses += 1
            # print(f"Guessing: {word}")
            for l in word:
                wordle.add_letter(l)
            
            done = wordle.enter_guess(benchmarking=True)
            if len(wordle.suggested_words) == 0:
                guesses = 6
                done = ReturnCodes.FINISHED
                continue
            word = choice(wordle.suggested_words)
        
        # if wordle.win:
        #     # print(f"Found the word in {guesses} guesses starting with {start}")
        #     pass
        # else:
        #     print(f"Lost with {start}")
        
        wordle.start()
        average += (guesses + 1)

    print(f"Average: {average / total}")


if __name__ == "__main__":
    main()