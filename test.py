from statistics import mean
from main import *


class WordGame:

    def __init__(self, words):
        self.word_list = words
        self.target_word = None
        self.word_length = None

    def set_target_word(self, target_word):
        self.target_word = target_word
        self.word_length = len(target_word)

    def check_guess(self, guess):
        if guess == self.target_word:
            return {"result": "correct"}

        guess = guess.lower()
        if len(guess) != self.word_length or guess not in self.word_list:
            raise ValueError(f"Guess must be a valid {self.word_length}-letter word")

        letter_info = []
        for index, letter in enumerate(guess):
            if letter == self.target_word[index]:
                letter_info.append({"letter": letter, "status": "correct"})
            elif letter in self.target_word:
                letter_info.append({"letter": letter, "status": "present"})
            else:
                letter_info.append({"letter": letter, "status": "incorrect"})

        return {"result": "incorrect", "letter_info": letter_info}


word_length = 5
words = get_words(5)
words_rating_original = get_words_rating(words)
word_game = WordGame(words)

results = []
i = 0
for word in words[:]:
    words_rating = words_rating_original.copy()
    word_game.set_target_word(word)
    tries = 1
    while True:
        response = word_game.check_guess(words_rating[0][0])
        if response['result'] == "correct":
            break
        tries += 1
        words_rating = filter_words_rating(response['letter_info'], words_rating)
    results.append(tries)
    i += 1

print(mean(results))
