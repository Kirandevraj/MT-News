from flask import Flask,render_template,request
import re
from googlesearch import search
from newspaper import Article

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
        return render_template('news.html', news1=articles[0], news2=articles[1], news3=articles[2])
    return render_template('query.html')
    
if __name__ == '__main__':
    app.run()