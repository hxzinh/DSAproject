from flask import render_template, Flask, request
import json
from trietree import TrieTree

app = Flask(__name__, static_folder="statics")

dictionary_av = {}
dictionary_va = {}

def Opendictionary(files):
    diction = dict()
    with open(f"database/{files}.json",'r') as file:
        diction = json.load(file)
    return diction

def InitTrie(trie, dictionary):
    for item in dictionary:
        word_i = item['word']
        pronunciation = item['pronunciation']
        definition = item['definition']
        trie.insert(word_i, pronunciation, definition)

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", boolean = True)

@app.route("/search", methods=["GET", "POST"])
def search():
    txt = ""
    trans_option = "" 

    if request.method == "POST":
        txt = request.form["txt"]
        trans_option = request.form["trans_option"]
    elif request.method == "GET":
        txt = request.args.get("txt")
        trans_option = request.args.get["trans_option"]

    print(txt)

    if trans_option == "anh-viet":
        word, pronunciation, definition = trie_av.find(txt)
    else:
        word, pronunciation, definition  = trie_va.find(txt)

    print(word, pronunciation, definition)

    definition = definition.replace("\n", "<br>")
    pronunciation = "/" + pronunciation + "/" if pronunciation != "" else ""

    return render_template(
        "result.html",
        word = word,
        pronunciation = pronunciation,
        definition = definition,
        trans_option = trans_option,
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
    
    app.run(host="0.0.0.0", port=5000, debug=True)