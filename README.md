# Wordle Solver

This project is a Python script designed to solve the popular word-guessing game, Wordle. The script leverages a custom scoring system to evaluate potential guesses and strategically filters words based on feedback from each guess. It interacts with a Wordle API to submit guesses and receive feedback.

## The evaluation function
Each letter is assigned a value (data was taken from the (wikipedia article)[https://en.wikipedia.org/wiki/Letter_frequency], the data was multiplied by a 1000 to avoid floating point errors). For each word that value is added to the word's score if it is the first occurence, else it is subtracted. Based on that evaluation all words are sorted, and the best one is chosen for a guess.

```py
def evaluate(word):
    result = 0
    letters = []
    for letter in word:
        if letter in letters:
            result -= letter_frequency[letter]
        else:
            result += letter_frequency[letter]
            letters.append(letter)
    return result
```

## What's next
The function still has much room for improvements. For example, if all letters are known but 1, and the list consists of multiple words, all the words will be checked with each check ruling out only 1 word. A better strategy would be to implement an evaluation system that would determine whether is better to try and guess the word, or gain more info about the letters.
