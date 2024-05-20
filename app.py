from flask import render_template, Flask, request, jsonify
import json
from trietree import TrieTree
from aho_croasick import AhoCroasick

app = Flask(__name__, static_folder="statics")

dictionary_av = {}
dictionary_va = {}
aho = {}

def Opendictionary(files):
    """
    Opens a JSON dictionary file and loads its content.

    Args:
        files (str): The name of the dictionary file (without extension).

    Returns:
        dict: The dictionary loaded from the JSON file.
    """
    diction = dict()
    with open(f"database/{files}.json",'r') as file:
        diction = json.load(file)
    return diction

def InitTrie(trie, dictionary):
    """
    Initializes a Trie tree with words, pronunciations, and definitions from a dictionary. Using Trie algorithm to optimize search time.

    Args:
        trie (TrieTree): The TrieTree instance to be initialized.
        dictionary (dict): The dictionary containing words, pronunciations, and definitions.
    """
    for item in dictionary:
        word_i = item['word']
        pronunciation = item['pronunciation']
        definition = item['definition']
        trie.insert(word_i, pronunciation, definition)

def InitAhoCroasick(dictionary):
    """
    Initializes an Aho-Corasick tree with words from a dictionary.

    Args:
        dictionary (dict): The dictionary containing words.
    
    Returns:
        AhoCorasick: The initialized AhoCorasick instance.
    """
    keywords = [item['word'] for item in dictionary]
    return AhoCroasick(keywords)

@app.route('/')
@app.route('/home')
def home():
    """
    Renders the home page of the application which contains the search form.

    Returns:
        str: The rendered HTML template for the home page.
    """
    return render_template("index.html", boolean = True)

@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Handles search requests, finds the word in the appropriate Trie, and renders the result page.

    Methods:
        GET, POST

    Returns:
        str: The rendered HTML template for the search results.
    """
    txt = ""
    trans_option = ""
    is_found = ""

    if request.method == "POST":
        txt = request.form["txt"]
        trans_option = request.form["trans_option"]
    elif request.method == "GET":
        txt = request.args.get("txt")
        trans_option = request.args.get("trans_option")

    if trans_option == "anh-viet":
        word, pronunciation, definition = trie_av.find(txt)
    else:
        word, pronunciation, definition = trie_va.find(txt)

    print(word)
    if word == "Not found":
        is_found = not_found(txt)
        is_found = ', '.join(is_found)

    definition = definition.replace("\n", "<br>")
    pronunciation = "/" + pronunciation + "/" if pronunciation != "" else ""

    return render_template(
        "result.html",
        word=word,
        pronunciation=pronunciation,
        definition=definition,
        trans_option=trans_option,
        not_found=is_found
    )

@app.route("/suggestion", methods=["GET"])
def suggestion():
    """
    Provides word suggestions based on the prefix entered by the user.

    Args:
        word (str): The prefix of the word to get suggestions for.
        translation_option (str): The translation option ("anh-viet" or "viet-anh").

    Returns:
        list: A list of up to 10 word suggestions matching the prefix.
    """
    word = request.args.get("word").lower()
    trans_option = request.args.get("trans_option")

    if not word or not trans_option:
        return []

    if trans_option == "anh-viet":
        data = trie_av.get_prefix(word)
    elif trans_option == "viet-anh":
        data = trie_va.get_prefix(word)
    return data[0:10]

#@app.route("/not_found", methods=["GET", "POST"])
def not_found(word):
    """
    Handles cases where a word is not found in the Trie.

    Args:
        word (str): The word to be searched in the Aho-Corasick structure.
        trans_option (str): The translation option ("anh-viet" or "viet-anh").

    Returns:
        list: A list of words from the Aho-Corasick search results.
    """

    data = aho.search(word)
    result = []
    for i, u in data:
        if len(u) >= 3 and u not in result:
            result.append(u)

    print(result)
    return result

if __name__ == '__main__':
    """
    The main execution block.

    Loads the dictionaries, initializes the Trie trees with data, and starts the Flask application.
    """
    dictionary_av = Opendictionary("dba-v")
    dictionary_va = Opendictionary("dbv-a")
    trie_av = TrieTree()
    trie_va = TrieTree()
    InitTrie(trie_av, dictionary_av)
    InitTrie(trie_va, dictionary_va)

    aho = InitAhoCroasick(dictionary_av)

    app.run(host="0.0.0.0", port=5000, debug=True)