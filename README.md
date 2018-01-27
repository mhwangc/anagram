# Anagram Finder

## Usage

To initialize the Anagram Finder, navigate to the folder containing `anagrams.py` and your input dictionary (a text file with a single dictionary entry on each line):
```
python anagrams.py <dictionary_file>
```

You may then enter words, and the program will print a list of anagrams of that word from the dictionary. Anagrams are case insensitive. `-` will be printed if no anagram exists. Press enter (i.e. an empty string) to exit the program.

## Design

Two words that are anagrams should have the same exact representation if we were to take the words and sort the characters within them in lexigraphical order. Therefore I decided to process all the words by converting them to lowercase, sorting the characters within each word lexigraphically, and then grouping words with the same lexigraphical sorting together (i.e. these words were anagrams of each other because they contain the same exact letters). These groupings were stored in a Trie. While reading input, the program will sort each read word and insert it into a Trie belonging to an AnagramFinder object. The position of the word in the Trie depends on its sorted self, but the actual word stored at the TrieNode is the original word. When we want to find a word and find its anagrams, we convert the word to lowercase, sort its letters, and traverse down the AnagramFinder's Trie.

I decided to use a Trie to store sorted words (and their anagrams), because Tries tend to be more elegant when dealing with large amounts of data that can have redundant elements (in this case, many words that share characters) as well as searching for words. Another alternative is a hashmap that maps sorted words to their anagrams, but both data structures require `Theta(N)` time to insert into and find words (where `N` is the length of the word). To find / insert a word in a Trie, we must traverse `O(N)` nodes, and to find / insert into a hashmap, we must hash the string which takes `Theta(N)` time. In addition, after the whole Trie is populated, I sort the list of words stored in each TrieNode as an additional post-processing that would make the online step quicker by avoiding the need to sort. Typically, this should be done at runtime and cached because not all nodes will be used and we would do needless work, but this makes the online runtime slightly faster.

Additionally, I tried to generalize my Trie and TrieNode classes as much as possible such that their usage could be essentially independent of our AnagramFinder (i.e. we could use the Trie and TrieNode classes for any other project with little modification).

## Runtime (Question 1)

### Offline

Let our dictionary have `N` words each with max length `M`.

We must read in `N` words and sort each one, which is `Theta(MlogM)` (actually we can do this in `Theta(M)` time if we use a radix sort, but the default Python list sort method is `Theta(MlogM)`). Inserting into a Trie is `Theta(M)`. The postprocessing where we sort the list of words stored at each TrieNode is a litle more difficult to calculate the runtime of because it depends on the number of nodes in our Trie, and the maximum number of elements stored in each TrieNode. There could be a maximum of ~M^27 TrieNodes, and a maximum of `N` words at a TrieNode, so the absolute worst case is that this step will take `O(M^27 NlogN)` time, but in reality this is very, very unlikely, and essentially impossible. The more likely scenario would be that there are a negligible amount of words at each TrieNode so sorting is essentially constant and the runtime would be absolute worst case `O(M^27)` just to explore our whole Trie.

Therefore, the offline step takes `Theta(N(MlogM))` time and additional time to process and sort each node (which I described above).

### Online
Let our dictionary have `N` and our input word have length `M`.

We first sort the input word which is `Theta(MlogM)` and then search for it in our trie which is `Theta(M)`. The total asymptotic runtime for searching is then `Theta(MlogM)`. If we were to use a radix sort, this would be 'Theta(M)', but the performance improvement is negligible when M <= 100.

## Memory (Question 2)
Let our dictionary have `N` and our words have length `M`. In our Trie, we will be storing N words. In the worst case, each TrieNode stores at most one word and each word requires M TrieNodes that are not shared with any other word. Therefore the space complexity is `Theta(N + MN)` which reduces to `Theta(MN)`. Realistically, it space requirements would be smaller because multiple words can be located at a TrieNode, and TrieNodes can be shared by multiple different anagrams.

## No Preprocessing (Question 3)
If we were unable to preprocess, we would have to process our dictionary on the fly each time we wanted to check an anagram. We know we have to at least read in every single word in the dictionary to check if our target word is an anagram of it, so the main issue is how to check if two words are anagrams of each other quickly. First, we can save the length of our target word, and for each word we are testing, do a constant time check to see if they are the same length. If they are not, we know they are not anagrams, and we move onto the next word. Secondly, we can convert our `Theta(MlogM)` algorithm of sorting a string and comparing the two together to a linear time two-pass algorithm. Instead of sorting our target word, we count how many of each letter the target word has. Then we do a pass through the word we are testing to count how many of each letter the word contains, and then we do a second "pass" where we compare the counts of the two words to check if they have the same counts. This would require a combination of hashmaps and arrays which may end up having more overhead then our original `Theta(MlogM)` sorting-and-checking algorithm, so for small M, this method may not be faster.