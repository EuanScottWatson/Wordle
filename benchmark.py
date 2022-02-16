from random import choice
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

from wordle import *

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


def best_word():
    wordle = Wordle()
    total = 50
    best = ("", float('inf'))
    for i, s in enumerate(wordle.words):
        sum = 0
        start = s.upper()
        for _ in range(total):
            word = start
            done = ReturnCodes.NEXT
            guesses = 0

            while done == ReturnCodes.NEXT:
                guesses += 1
                for l in word:
                    wordle.add_letter(l)
                
                done = wordle.enter_guess(benchmarking=True)
                if len(wordle.suggested_words) == 0:
                    guesses = 6
                    done = ReturnCodes.FINISHED
                    continue
                word = choice(wordle.suggested_words)
            
            wordle.start()
            sum += (guesses + 1)

        avg = sum / total
        if avg < best[1]:
            best = (start, avg)
        
        print("%.2f percent complete. Best: %s -> %f" % (
            round(i / len(wordle.words) * 100, 3),
            best[0],
            best[1]
        ), end='\r')
        sys.stdout.flush()


guesses_tally = [0 for _ in range(7)]
x = list(range(1, 8))

def all(i):
    wordle = Wordle()

    word = choice(wordle.words).upper()
    done = ReturnCodes.NEXT
    guesses = 0

    while done == ReturnCodes.NEXT:
        guesses += 1
        for l in word:
            wordle.add_letter(l)
        
        done = wordle.enter_guess(benchmarking=True)
        if len(wordle.suggested_words) == 0:
            guesses = 6
            done = ReturnCodes.FINISHED
            continue
        word = choice(wordle.suggested_words)
    
    wordle.start()

    guesses_tally[guesses] += 1

    ax1.clear()
    ax1.bar(x, guesses_tally)



def main():
    if sys.argv[1] == "-best":
        best_word()
    elif sys.argv[1] == "-all":
        ani = animation.FuncAnimation(fig, all, interval=10)
        plt.show()


if __name__ == "__main__":
    main()