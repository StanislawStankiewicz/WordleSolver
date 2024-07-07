import requests
from evaluate import evaluate


def filter_word(word, letter_info):
    for i in range(len(word)):
        letter = word[i]
        guess_letter = letter_info[i]['letter']
        status = letter_info[i]['status']
        if status == 'incorrect' and guess_letter in word:
            return False
        if status in ['present', 'correct'] and guess_letter not in word:
            return False
        if status == 'correct' and letter != guess_letter:
            return False
    return True


BASE_URL = 'http://localhost:5000'
API_ENDPOINT = "/api/wordle"
WORDLENGTH_URL = BASE_URL + API_ENDPOINT + "/wordlength"
GUESS_URL = BASE_URL + API_ENDPOINT + "/guess"

wordLength = requests.get(WORDLENGTH_URL).json()['wordLength']
with open('resources/words.txt', 'r') as file:
    words = [word.strip() for word in file.readlines()]
words = list(filter(lambda word: len(word) == wordLength, words))

words_rating = []
for word in words:
    words_rating.append([word, evaluate(word)])
words_rating.sort(key=lambda pair: pair[1], reverse=True)

response = requests.post(GUESS_URL,
                         json={"guess": words_rating[0][0]},
                         headers={"Content-Type": "application/json"}).json()
print("Sending guess:", words_rating[0][0])

while response['result'] == "incorrect":
    words_rating = list(filter(lambda word: filter_word(word[0], response["letter_info"]), words_rating))
    print("Sending guess:", words_rating[0][0])
    response = requests.post(GUESS_URL,
                             json={"guess": words_rating[0][0]},
                             headers={"Content-Type": "application/json"}).json()
