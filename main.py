from collections import Counter
from enum import Enum


class BIBLES(Enum):
    ERV = "English Revised Version"
    KJV = "King James Version"

    def filename(self):
        return self.name.lower() + ".txt"


def clean_line(line: str) -> list[str]:
    cleaned_line = []
    current_word = []
    for c in line:
        if c in [" ", "\n"] and current_word:
            cleaned_line.append("".join(current_word))
            current_word = []
        elif c.isalpha():
            current_word.append(c.lower())

    if current_word:
        cleaned_line.append("".join(current_word))

    return cleaned_line


def least(counter: Counter, n: int) -> list:
    return counter.most_common()[-n:]


def with_count_of(words: Counter, minimum: int, maximum: int) -> list:
    word_list = []
    for word, count in words.most_common():
        if minimum <= count <= maximum:
            word_list.append((word, count))

    return word_list


def words_in_bible(words: Counter, text: str):
    cleaned_text = clean_line(text)
    return [(word, word in words) for word in cleaned_text]


def check_text(words: Counter, text):
    words_truth = words_in_bible(words, text)
    in_bible = [p[0] for p in words_truth if p[1]]
    not_in_bible = [p[0] for p in words_truth if not p[1]]
    percentage = len(in_bible) / len(words_truth) * 100

    print("In Bible:")
    for w in in_bible:
        print("    " + w)

    print()
    print("Not in Bible:")
    for w in not_in_bible:
        print("    " + w)

    print()
    print(f"Percentage of words in bible: {percentage}%")


def main():
    words = Counter()

    with open("bibles/kjv.txt", encoding="utf-8-sig") as f:
        while line := f.readline():
            words.update(clean_line(line))

    nfts = "Fox is making a blockchain animated series with Rick and Morty creator Dan Harmon to sell you NFTs"

    # check_text(words, nfts)
    with open("timecube.txt") as f:
        time = f.read()
        check_text(words, time)
    # print(with_count_of(words, 2, 3))
    # print(least(words, 10))
    # print(words.most_common())

    # print(words["slaves"])


# def in_bible(string)

if __name__ == "__main__":
    main()
