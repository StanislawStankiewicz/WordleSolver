import yaml

with open('resources/letter_frequency.yml', 'r') as file:
    letter_frequency = yaml.safe_load(file)


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
