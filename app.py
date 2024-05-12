from flask import Flask,render_template, request, url_for, redirect

app = Flask(__name__)

import lucene
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import RAMDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.document import Document, StringField, TextField
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from threading import local

import os
import json

import sys


def index_corpus(corpus_dir, writer):
    for filename in os.listdir(corpus_dir):
        filepath = os.path.join(corpus_dir, filename)

        doc = Document()
        with open(filepath, 'r') as f:
            data = json.load(f)
            #print(f"\nPost from {filename} by {data['author']}:")

            doc.add(TextField("title", data['title'], Field.Store.YES))
            doc.add(TextField("post_url", data['post_url'], Field.Store.YES))
            doc.add(TextField("filepath", filepath, Field.Store.YES))
            doc.add(TextField("body", data['body'], Field.Store.YES))
        
            content = ""
            for comment in data['comments']:
                content += comment['body']

            doc.add(TextField("content", content, Field.Store.YES))
            
            writer.addDocument(doc)
        writer.commit()

def search(index_dir, query, max_results):
    reader = DirectoryReader.open(index_dir)
    searcher = IndexSearcher(reader)

    analyzer = StandardAnalyzer()
    q = QueryParser("content", analyzer).parse(query)

    hits = searcher.search(q, max_results)

    results = []
    for hit in hits.scoreDocs:
        doc = searcher.doc(hit.doc)
    #results.append((doc.get("body"), hit.score))
        results.append((doc.get("title"), hit.score, doc.get("post_url")))

    reader.close()
    return results

def to_html(results):
    html = ""
    for idx, result in enumerate(results):
        title = result[0]
        score = result[1]
        url   = result[2]
        html += f"""<tr>
            <th scope="row">{idx+1}</th>
            <td colspan="2"><a href="{url}">{title}</a></td>
            <td>{score}</td>
        </tr>
        """
    return html

lucene.initVM()

index_dir = RAMDirectory()
analyzer = StandardAnalyzer()
writer_config = IndexWriterConfig(analyzer)
writer = IndexWriter(index_dir, writer_config)
index_corpus("./RedditParser/data2", writer)

@app.route("/", methods=["POST","GET"])
def home():
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()

    if request.method == "POST":
        search_input = request.form.get('searchInput')
        return render_template("index.html", result = to_html(search(index_dir, search_input, 200)))
    else:
        return render_template("index.html", result = "")

@app.route("/<sinput>")
def input(sinput):
    print("hello sinput", file=sys.stderr)
    return render_template("index.html", result = to_html(search(ind, sinput, 10)))

if __name__ == "__main__":
    app.run(debug=False)