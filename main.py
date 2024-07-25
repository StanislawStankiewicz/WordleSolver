import requests
from evaluate import evaluate


def filter_word(word, letter_info):
    for i in range(len(word)):
        letter = word[i]
        guess_letter = letter_info[i]['letter']
        status = letter_info[i]['status']
        if letter == guess_letter and status == 'present':
            return False
        if status == 'incorrect' and guess_letter in word:
            return False
        if status in ['present', 'correct'] and guess_letter not in word:
            return False
        if status == 'correct' and letter != guess_letter:
            return False
    return True


def get_word_length():
    return requests.get(WORDLENGTH_URL).json()['wordLength']


def get_guess(words_rating):
    return requests.post(GUESS_URL,
                         json={"guess": words_rating[0][0]},
                         headers={"Content-Type": "application/json"}).json()


def get_words(word_length=5):
    with open('resources/words.txt', 'r') as file:
        words = [word.strip() for word in file.readlines()]
    return list(filter(lambda word: len(word) == word_length, words))


def get_words_rating(words):
    words_rating = []
    for word in words:
        words_rating.append([word, evaluate(word)])
    words_rating.sort(key=lambda pair: pair[1], reverse=True)
    return words_rating


def filter_words_rating(letter_info, words_rating):
    return list(filter(lambda word: filter_word(word[0], letter_info), words_rating))


BASE_URL = 'http://54.226.222.83'
API_ENDPOINT = "/api/wordle"
WORDLENGTH_URL = BASE_URL + API_ENDPOINT + "/wordlength"
GUESS_URL = BASE_URL + API_ENDPOINT + "/guess"

if __name__ == '__main__':
    word_length = get_word_length()
    words = list(filter(lambda word: len(word) == word_length, get_words()))
    words_rating = get_words_rating(words)

    while True:
        print("Sending guess:", words_rating[0][0])
        response = get_guess(words_rating)
        if response['result'] == "correct":
            break
        words_rating = filter_words_rating(response['letter_info'], words_rating)
