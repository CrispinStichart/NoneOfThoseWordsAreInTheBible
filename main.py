from collections import Counter
from enum import Enum
from dataclasses import dataclass
import json

BIBLES_DIR = "bibles"


class BIBLES(Enum):
    ERV = "English Revised Version"
    KJV = "King James Version"

    def filename(self):
        return self.name.lower() + ".txt"


@dataclass
class Result:
    bible: "Bible"
    text: str
    in_bible: list["Word"]
    not_in_bible: list[str]
    percentage: float

    def to_dict(self) -> dict:
        words_in_bible = [word.to_dict() for word in self.in_bible]
        return {
            "version": str(self.bible.bible_version),
            "original_text": self.text,
            "words_in_bible": words_in_bible,
            "words_not_in_bible": self.not_in_bible,
            "percentage_of_words_in_bible": self.percentage,
        }


class Verse:
    """
    Note that verses are not comparable across versions, since versions differ
    slightly in their verses. See:
    https://en.wikipedia.org/wiki/List_of_New_Testament_verses_not_included_in_modern_English_translations


    The `index` is the absolute position in the complete list of verses. Again,
    this is only valid for a particular version.
    """

    def __init__(self, book_name: str, chapter_num: int, verse_num: int, index: int):
        self.book_name = book_name
        self.chapter_num = chapter_num
        self.verse_num = verse_num
        self.index = index

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return f"{self.book_name}, {self.chapter_num}:{self.verse_num}"

    def to_dict(self) -> dict:
        return {
            "book_name": self.book_name,
            "chapter_num": self.chapter_num,
            "verse_num": self.verse_num,
            "index": self.index,
        }

    @staticmethod
    def from_string(info: str, line_no: int) -> "Verse":
        # Format: <Book> <chapter num>:<verse num>
        book_and_chapter, verse_num = info.split(":")
        # Since some books (e.g. 1 Samuel) have a space in them, we need to
        # split and then rejoin all but the last element.
        book_and_chapter = book_and_chapter.split()
        book_name = " ".join(book_and_chapter[:-1])
        chapter_num = book_and_chapter[-1]

        verse = Verse(book_name, int(chapter_num), int(verse_num), line_no)
        return verse


class Word:
    def __init__(self, word: str, verse_id: Verse):
        self.word: str = word
        self.contained_in_verses: set[Verse] = {verse_id}
        self.count: int = 1

    def update(self, verse_id: Verse):
        self.contained_in_verses.add(verse_id)
        self.count += 1

    def to_dict(self) -> dict:
        return {
            "word": self.word,
            "contained_in_verses": [
                verse.to_dict() for verse in self.contained_in_verses
            ],
        }


class Bible:
    def __init__(self, bible_version: BIBLES):
        self.words: dict[str, Word] = {}
        self.bible_version = bible_version
        self.verses: list[str] = []

        self.read_bible()

    def read_bible(self):
        with open(BIBLES_DIR + "/" + self.bible_version.filename()) as f:
            # There are metadata lines at the start of each file, so we skip them.
            f.readline()
            f.readline()

            self.verses = f.readlines()
            for line_no, line in enumerate(self.verses):
                # One verse per line. The format is:
                #   <Book> <chapter num>:<verse num>\t<text>
                verse_id, full_verse = line.split("\t")
                word_list = clean_line(full_verse)
                verse_id = Verse.from_string(verse_id, line_no)
                # Add or update the word.
                for word in word_list:
                    if word in self.words:
                        self.words[word].update(verse_id)
                    else:
                        self.words[word] = Word(word, verse_id)

    def check_text_and_print(self, text: str) -> None:
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

    def check_text(self, text: str) -> Result:
        cleaned_text = clean_line(text)
        in_bible = [self.words[word] for word in cleaned_text if word in self.words]
        not_in_bible = [word for word in cleaned_text if word not in self.words]
        percentage = len(in_bible) / len(cleaned_text) * 100
        return Result(self, text, in_bible, not_in_bible, percentage)


def clean_line(line: str) -> set[str]:
    cleaned_line = set()
    current_word = []
    for c in line:
        if c in [" ", "\n"] and current_word:
            cleaned_line.add("".join(current_word))
            current_word = []
        elif c.isalpha():
            current_word.append(c.lower())

    if current_word:
        cleaned_line.add("".join(current_word))

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
    bible = Bible(BIBLES.KJV)

    nfts = "Fox is making a blockchain animated series with Rick and Morty creator Dan Harmon to sell you NFTs"

    r = bible.check_text("fox dan morty")
    print(json.dumps(r.to_dict(), indent=2))
    # bible.check_text_and_print(nfts)
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
