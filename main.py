from collections import Counter
from enum import Enum

BIBLES_DIR = "bibles"


class BIBLES(Enum):
    ERV = "English Revised Version"
    KJV = "King James Version"

    def filename(self):
        return self.name.lower() + ".txt"


class Word:
    def __init__(self, word: str, verse_id: str):
        self.word: str = word
        self.contained_in_verses: set[str] = {verse_id}
        self.count: int = 1

    def update(self, verse_id: str):
        self.contained_in_verses.add(verse_id)
        self.count += 1


class BibleWords:
    def __init__(self, bible_version: BIBLES):
        self.words: dict[str, Word] = {}
        self.bible_version = bible_version

        self.read_bible()

    def read_bible(self):
        with open(BIBLES_DIR + "/" + self.bible_version.filename()) as f:
            # There are metadata lines at the start of each file, so we skip them.
            f.readline()
            f.readline()

            while line := f.readline():
                # One verse per line. The format is:
                #   <Book> <chapter num>:<verse num>\t<text>
                verse_id, text = line.split("\t")
                text = clean_line(line)
                # Add or update the word.
                for word in text:
                    if word in self.words:
                        self.words[word].update(verse_id)
                    else:
                        self.words[word] = Word(word, verse_id)

    def check_text(self, text: str):
        cleaned_text = clean_line(text)
        words_truth = [(word, word in self.words) for word in cleaned_text]
        in_bible = [p[0] for p in words_truth if p[1]]
        not_in_bible = [p[0] for p in words_truth if not p[1]]
        percentage = len(in_bible) / len(words_truth) * 100

        print(f"In Bible ({self.bible_version.value}):")
        for w in in_bible:
            print(f"\t{w} (in {len(self.words[w].contained_in_verses)} verses)")

        print()
        print("Not in Bible:")
        for w in not_in_bible:
            print("    " + w)

        print()
        print(f"Percentage of words in bible: {percentage:.1f}%")


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


def main():
    bible = BibleWords(BIBLES.KJV)

    nfts = "Fox is making a blockchain animated series with Rick and Morty creator Dan Harmon to sell you NFTs"

    bible.check_text(nfts)
    # with open("timecube.txt") as f:
    #     time = f.read()
    #     check_text(words, time)
    # print(with_count_of(words, 2, 3))
    # print(least(words, 10))
    # print(words.most_common())

    # print(words["slaves"])


# def in_bible(string)

if __name__ == "__main__":
    main()
