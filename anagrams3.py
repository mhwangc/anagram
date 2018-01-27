import sys

class AnagramFinder:

    def __init__(self, filename):
        self.filename = filename
        self.word_trie = Trie()
        self.read_words()

    def read_words(self):
        input_file = open(self.filename, "r")
        for line in input_file:
            word = line.strip()
            sorted_word = "".join(sorted(word.lower()))
            self.word_trie.insert(sorted_word, word)
        self.word_trie.sort_lists()

    def find_anagrams(self, word):
        sorted_word = "".join(sorted(word.lower()))
        return self.word_trie.find(sorted_word)

class Trie:

    def __init__(self):
        self.top_node = TrieNode("")

    # inserts a word into the Trie
    def insert(self, key, word):
        self.top_node.insert(key, word, 0)

    # returns list of words that are anagrams of word, or empty list if none
    def find(self, word):
        return self.top_node.find(word, 0)

    # sorts all lists of words in the Trie
    def sort_lists(self):
        self.top_node.sort_words()

class TrieNode:

    def __init__(self, letter):
        self.letter = letter
        self.children = {}
        self.words = []

    def insert(self, suffix, word, index):
        if len(suffix) == index:
            self.words.append(word)
        else:
            first = suffix[index]
            if first not in self.children:
                self.children[first] = TrieNode(first)
            self.children[first].insert(suffix, word, index + 1)

    def find(self, suffix, index):
        if len(suffix) == index:
            return self.words
        elif suffix[index] in self.children:
            return self.children[suffix[index]].find(suffix, index + 1)
        else:
            return []

    def sort_words(self):
        self.words.sort()
        for child in self.children:
            self.children[child].sort_words()

def main():
    filename = sys.argv[1]
    finder = AnagramFinder(filename)
    while True:
        test_word = input()
        if test_word == "":
            break
        else:
            words = finder.find_anagrams(test_word)
            if not words:
                print("-")
            else:
                print(" ".join(words))


if __name__ == "__main__":
    main()