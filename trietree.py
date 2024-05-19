#---------------------------------Trie-------------------------------------------#
class TrieNode:
    """
    A node in the Trie structure.

    Attributes:
        text (str): The text represented by this node.
        pronunciation (str): The pronunciation of the word ending at this node.
        definition (str): The definition of the word ending at this node.
        children (dict): A dictionary mapping each character to its corresponding TrieNode.
        is_end_of_word (bool): A flag indicating if this node marks the end of a word.
    """

    def __init__(self, text = '', pronunciation='', definition=''):
        self.children = dict()
        self.text = text
        self.is_end_of_word = False
        self.pronunciation = pronunciation
        self.definition = definition

class TrieTree:
    """
    A Trie (prefix tree) for storing strings with additional information.

    Methods:
        insert(word, pronunciation, definition):
            Inserts a word along with its pronunciation and definition into the Trie.
        find(word):
            Finds and returns the word, pronunciation, and definition if the word exists in the Trie.
        get_child(current_node, words):
            Recursively collects all words that are children of the current node.
        get_prefix(prefix):
            Returns all words in the Trie that start with the given prefix.
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, pronunciation, definition):
        """
        Inserts a word into the Trie with its pronunciation and definition.

        Args:
            word (str): The word to insert.
            pronunciation (str): The pronunciation of the word.
            definition (str): The definition of the word.
        """

        current_node = self.root
        for i, char in enumerate(word):
            if char not in current_node.children:
                current_node.children[char] = TrieNode(word[0:i+1])
            current_node = current_node.children[char]
        current_node.is_end_of_word = True
        current_node.pronunciation = pronunciation
        current_node.definition = definition

    def find(self, word):
        """
        Finds a word in the Trie and returns its text, pronunciation, and definition.

        Args:
            word (str): The word to find.

        Returns:
            tuple: A tuple containing the text, pronunciation, and definition of the word. 
                   If the word is not found, returns ("Not found", "", "").
        """

        current_node = self.root
        for char in word:
            if char not in current_node.children:
                return "Not found", "", ""
            current_node = current_node.children[char]
        if current_node.is_end_of_word:
            return current_node.text, current_node.pronunciation, current_node.definition
        else:
            return "Not found", "", ""
        
    def get_child(self, current_node, words):
        """
        Recursively collects all words that are children of the current node.

        Args:
            current_node (TrieNode): The node from which to collect words.
            words (list): The list to which collected words are appended.
        """

        if current_node.is_end_of_word:
            words.append(current_node.text)
        for letter in current_node.children:
            self.get_child(current_node.children[letter], words)

    def get_prefix(self, prefix):
        """
        Returns all words in the Trie that start with the given prefix.

        Args:
            prefix (str): The prefix to search for.

        Returns:
            list: A list of words starting with the given prefix.
        """
    
        words = list()
        current_node = self.root
        for char in prefix:
            if char not in current_node.children:
                return list()
            current_node = current_node.children[char]
        self.get_child(current_node, words)
        return words
