"use strict";

let bible = new Bible(kjv)

function submitButtonClicked() {
    let text = document.getElementById("textbox").value;
    checkText(text)
    document.getElementById("inputContainer").hidden = true;
    document.getElementById("resultsContainer").hidden = false;
}

function resetInput() {
    document.getElementById("textbox").value = "";
    document.getElementById("inputContainer").hidden = false;
    document.getElementById("resultsContainer").hidden = true;
    document.getElementById("wordsNotInBible").innerHTML = "";
    document.getElementById("wordsInBible").innerHTML = "";


}

function checkText(text) {
    let words = extract_unique_words(text);
    let in_bible = []
    let not_in_bible = []
    words.forEach((word) => {
        if (word in bible.words) {
            in_bible.push(bible.words[word])
        } else {
            not_in_bible.push(word)
        }
    });

    displayWords(in_bible)
    let wordsNotInBibleList = document.getElementById("wordsNotInBible")
    not_in_bible.forEach((word) => {
        let li = document.createElement("li");
        let text = document.createTextNode(word)
        li.appendChild(text);
        wordsNotInBibleList.appendChild(li)
    });

    document.getElementById("allWordsInBible").hidden = not_in_bible.length !== 0
    document.getElementById("clickWordsMsg").hidden = in_bible.length === 0
    document.getElementById("noWordsInBible").hidden = in_bible.length !== 0


}

function displayWords(words) {
    const resultsDiv = document.getElementById('wordsInBible');
    const list = document.createElement('ul');

    words.forEach(word => {
        const listItem = document.createElement('li');
        const text = document.createElement('span');
        text.classList.add("clickable");
        text.textContent = `"${word.word}" appears in ${word.containedInVerses.size} verses`;
        listItem.appendChild(text);
        // Click event to toggle display of verses
        text.addEventListener('click', function () {
            // Check if the details are already displayed
            if (listItem.childNodes.length > 1) {
                listItem.removeChild(listItem.lastChild);  // Toggle off, remove the sublist
            } else {
                // Create a nested list to show verses
                const verseList = document.createElement('ul');

                word.containedInVerses.forEach(verseId => {
                    verseList.appendChild(createVerseListItem(verseId, word));
                });

                listItem.appendChild(verseList);  // Append the sublist to the list item
            }
        });

        list.appendChild(listItem);
    });

    resultsDiv.appendChild(list);
}

function createVerseListItem(verseId, word) {
    const verseItem = document.createElement('li');
    const verse = bible.verses[verseId.index]; // Access the verse using index
    const verseIdElement = document.createElement("em")
    const verseTextElement = document.createElement("span")

    verseIdElement.textContent = verseId.toString();
    verseTextElement.innerHTML = highlightWord(verse.text, word.word);
    verseItem.appendChild(verseIdElement);
    verseItem.appendChild(verseTextElement);

    return verseItem
}

/**
 * Highlights all occurrences of a word in a text string with bold tags.
 *
 * @param {string} text - The full text of the verse.
 * @param {string} word - The word to be highlighted.
 * @return {string} The text with the word highlighted in bold.
 */
function highlightWord(text, word) {
    const regex = new RegExp(`\\b${word}\\b`, 'gi'); // Case-insensitive, whole word match
    return text.replace(regex, match => `<strong>${match}</strong>`);
}