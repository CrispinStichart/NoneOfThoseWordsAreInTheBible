/**
 * Just for the identification part of the verse, and not the full line.
 */
class VerseId {
    /**
     * @param {string} bookName - The name of the book.
     * @param {number} chapterNum - The chapter number.
     * @param {number} verseNum - The verse number.
     * @param {number} index - The index in the list of verses.
     */
    constructor(bookName, chapterNum, verseNum, index) {
        this.bookName = bookName;
        this.chapterNum = chapterNum;
        this.verseNum = verseNum;
        this.index = index;
    }

    toString() {
        return `${this.bookName}, ${this.chapterNum}:${this.verseNum}`;
    }

}


/**
 * Note that verses are not comparable across versions, since versions differ
 * slightly in their verses. See:
 * https://en.wikipedia.org/wiki/List_of_New_Testament_verses_not_included_in_modern_English_translations
 * The `index` is the absolute position in the complete list of verses. Again,
 * this is only valid for a particular version.
 */
class Verse {
    /**
     * @param {string} text - The verse text.
     * @param {string} bookName - The name of the book.
     * @param {number} chapterNum - The chapter number.
     * @param {number} verseNum - The verse number.
     * @param {number} index - The index in the list of verses.
     */
    constructor(text, bookName, chapterNum, verseNum, index) {
        this.text = text;
        this.verseId = new VerseId(bookName, chapterNum, verseNum, index);
    }


    toString() {
        return `${this.verseId}\t${this.text}`;
    }

    /**
     * Create a Verse object from a string line.
     * @param {string} line - The line of text representing a verse.
     * @param {number} lineNo - The line number.
     * @return {Verse} The created Verse object.
     */
    static fromString(line, lineNo) {
        const [verseId, fullVerse] = line.split("\t");
        const [bookAndChapter, verseNum] = verseId.split(":");
        const bookAndChapterParts = bookAndChapter.split(" ");
        const chapterNum = bookAndChapterParts.pop();
        const bookName = bookAndChapterParts.join(" ");

        return new Verse(
            fullVerse.trim(),
            bookName,
            parseInt(chapterNum, 10),
            parseInt(verseNum, 10),
            lineNo
        );
    }
}

/**
 * Represents a word in a verse.
 */
class Word {
    /**
     * @param {string} word - The word string.
     * @param {VerseId} verseId - The verse identifier where the word was found.
     */
    constructor(word, verseId) {
        this.word = word;
        this.containedInVerses = new Set([verseId]);
        this.count = 1;
    }

    /**
     * Update the word with a new verse identifier.
     * @param {VerseId} verseId - The verse identifier where the word was found.
     */
    update(verseId) {
        this.containedInVerses.add(verseId);
        this.count += 1;
    }
}

/**
 * Represents a Bible.
 */
class Bible {
    /**
     * @param {string} bibleText - the text of the Bible.
     */
    constructor(bibleText) {
        this.words = {};
        this.bibleVersion = "";
        this.verses = [];

        this.readBible(bibleText);
    }

    /**
     * Read the Bible file and populate verses and words.
     * @param {string} bibleText - the text of the Bible.
     */
    readBible(bibleText) {
        const lines = bibleText.split("\n")
        this.bibleVersion = lines[1].trim();

        // Subtracting 1 because the last line will be empty, due to the files
        // ending with a newline.
        for (let i = 2; i < lines.length - 1; i++) {
            let line = lines[i];
            const verse = Verse.fromString(line, i - 2);
            this.verses.push(verse);
            const wordList = extract_unique_words(verse.text);

            wordList.forEach(word => {
                if (this.words[word]) {
                    this.words[word].update(verse.verseId);
                } else {
                    this.words[word] = new Word(word, verse.verseId);
                }
            });
        }
    }
}

/**
 * Extracts unique words.
 *
 * @param {string} line - The input string to clean.
 * @return {Set<string>} A set of unique lowercase words.
 */
function extract_unique_words(line) {
    const uniqueWords = new Set();

    const words = line.split(/\s+/); // Split by whitespace

    for (const word of words) {
        const cleanedWord = word.replace(/[^a-zA-Z]/g, "").toLowerCase();
        if (cleanedWord) {
            uniqueWords.add(cleanedWord);
        }
    }

    return uniqueWords;
}
