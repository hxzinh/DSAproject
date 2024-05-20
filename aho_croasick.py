class AhoNode:
    """
    A node in the Aho-Corasick trie.

    Attributes:
        children (dict): A dictionary mapping characters to child nodes.
        failure_link (AhoNode): A reference to the node where the algorithm should jump in case of a failure.
        output (list): A list of keywords that end at this node.
    """
    def __init__(self):
        self.children = {}
        self.failure_link = None
        self.output = []

class AhoCroasick:
    """
    A class implementing the Aho-Corasick string matching algorithm.

    Attributes:
        root (AhoNode): The root node of the Aho-Corasick trie.
    """
    def __init__(self, keywords):
        """
        Initializes the Aho-Corasick trie with the given keywords and builds failure links.

        Args:
            keywords (list): A list of strings to search for.
        """
        self.root = AhoNode()
        self.build_aho(keywords)
        self.build_failure_links()

    def build_aho(self, keywords):
        """
        Builds the Aho-Corasick trie by adding each keyword to the trie.

        Args:
            keywords (list): A list of strings to add to the trie.
        """
        for keyword in keywords:
            node = self.root
            for char in keyword:
                if char not in node.children:
                    node.children[char] = AhoNode()
                node = node.children[char]
            node.output.append(keyword)

    def build_failure_links(self):
        """
        Builds the failure links in the Aho-Corasick trie using a breadth-first search.
        """
        from collections import deque
        queue = deque()
        
        # Initialize the root's children
        for char, node in self.root.children.items():
            node.failure_link = self.root
            queue.append(node)
        
        # Breadth-first search to build failure links
        while queue:
            current_node = queue.popleft()
            
            for char, child_node in current_node.children.items():
                queue.append(child_node)
                fail = current_node.failure_link
                while fail is not None and char not in fail.children:
                    fail = fail.failure_link
                child_node.failure_link = fail.children[char] if fail else self.root
                child_node.output += child_node.failure_link.output

    def search(self, text):
        """
        Searches for keywords in the given text using the Aho-Corasick algorithm.

        Args:
            text (str): The text to search for keywords.

        Returns:
            list: A list of tuples containing the starting index and the matched keyword.
        """
        node = self.root
        results = []
        
        for i, char in enumerate(text):
            while node is not None and char not in node.children:
                node = node.failure_link
            if node is None:
                node = self.root
                continue
            node = node.children[char]
            if node.output:
                for pattern in node.output:
                    results.append((i - len(pattern) + 1, pattern))
        return results
