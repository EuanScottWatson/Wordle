from random import choice
import matplotlib.pyplot as plt

from wordle import *

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def best_word():
    # Runs `total` games of Wordle with each word to get the average number of guesses
    # needed to solve the game when starting with said word
    # Uses this tally to see which word is best to start with on average
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

            # Playing the game until word is found or lost
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

        printProgressBar(i + 1, len(wordle.words), suffix=f"Best: {best[0]} -> {best[1]}")


def all(total=1000):
    # Determines number of guesses needed on average for this method of advising
    # Picks next word to guess at random from the list of suggested words
    wordle = Wordle()

    guesses_tally = [0 for _ in range(7)]
    x = list(range(1, 8))
    
    for i in range(total):
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

        avg = sum(map(lambda g: (g[0] + 1) * g[1], enumerate(guesses_tally))) / (i + 1)
        printProgressBar(i + 1, total, suffix=f"Current Average: {round(avg, 2)}")

    # Plot the games
    ax1.bar(x, guesses_tally)


def main():
    # Use tag -best to find the best word and the tag -all to benchmark the strategy
    if sys.argv[1] == "-best":
        best_word()
    elif sys.argv[1] == "-all":
        if len(sys.argv) > 2:
            try:
                all(int(sys.argv[2]))
            except:
                print(f"Invalid argument: {sys.argv[2]}")
        else:
            all()
        plt.show()


if __name__ == "__main__":
    main()