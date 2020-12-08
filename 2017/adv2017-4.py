#!/usr/bin/python


def passphrase_words(passphrase):
    return passphrase.split(' ')


def unique_words(words):
    return set(words)


def valid_passphrase(passphrase):
    words = passphrase_words(passphrase)
    unique = unique_words(words)
    print passphrase, len(words), len(unique)
    return len(words) == len(unique)


def unique_words_with_anagrams(words):
    words = (''.join(word) for word in map(sorted, words))
    return set(words)


def valid_passphrase_with_anagrams(passphrase):
    words = passphrase_words(passphrase)
    unique = unique_words_with_anagrams(words)
    print passphrase, len(words), len(unique)
    return len(words) == len(unique)


if __name__ == '__main__':
    with open('adv2017-4.input') as input:
        print sum(map(int, (valid_passphrase(pf.strip()) for pf in input)))
    with open('adv2017-4.input') as input:
        print sum(map(int, (valid_passphrase_with_anagrams(pf.strip()) for pf in input)))
