from flask import Flask,render_template,request
import re
from googlesearch import search
from newspaper import Article
from urllib.request import urlopen
import urllib
import re
import json


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        query = request.form['query']
        results = []
        query = query + ' site:thehindu.com'
        for x in search(query, tld="co.in", num=3, stop=1, pause=2):
            results.append(x)
        articles = []
        for url in results:
            article = Article(url)
            article.download()
            article.parse()
            news = re.sub("\n"," ", article.text)
            news = article.title + " : " + news
            articles.append(news)
        def repl(matchobj):
            if matchobj.group(0) !=". ": 
                return matchobj.group(0)
            if matchobj.group(1): 
                return matchobj.group(1)+"\r"
            if matchobj.group(2): 
                return matchobj.group(2)+"\r"
        trans = []
        for art in articles:
            q_list = art.split('\n')
            sentences = []
            translation = ''
            for each in q_list:
                if each != '':
                    sentences = sentences + (re.sub(r'\b(\w\.\w\.)|([.?!])\s+(?=[A-Za-z])', repl, each)).split("\r")
            for x in sentences:
                f = {'q':x}
                query = urllib.parse.urlencode(f)
                page_url = "http://preon.iiit.ac.in/babel?" + query
                try:
                    response = urlopen(page_url)
                    #    if 'text/html' in response.getheader('Content-Type'):
                    html_bytes = response.read()
                    html_string = html_bytes.decode("utf-8")
                    jobj = json.loads(html_string)
                    translation = translation + jobj[0]["hypotheses"][0]["prediction_raw"]
                except:
                    print("error")
            trans.append(translation)
        return render_template('news.html', news1=articles[0],trans1=trans[0], news2=articles[1],trans2 = trans[1], news3=articles[2],trans3=trans[2])
    return render_template('query.html')
    
if __name__ == '__main__':
    app.run()