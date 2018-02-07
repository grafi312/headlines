import feedparser

from flask import Flask

app = Flask(__name__)

RSS_FEEDS = {
    "bbc": "http://feeds.bbci.co.uk/news/rss.xml",
    "cnn": "http://rss.cnn.com/rss/edition.rss",
    "fox": "http://feeds.foxnews.com/foxnews/latest",
    "iol": "http://www.iol.co.za/cmlink/1.640"
}

@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed["entries"][0]

    return """
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Headlines</title>
</head>
<body>
    <h1>Headlines</h1>
    <h4>{0}</h4>
    <i>{1}</i>
    <p>{2}</p>
</body>
</html>
    """.format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))

if __name__ == "__main__":
    app.run(port=5000, debug=True)