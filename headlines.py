import json
import urllib
import feedparser

from flask import Flask, render_template, request

app = Flask(__name__)

DEFAULTS = {
    "publication": "bbc",
    "city": "Bishkek,Kyrgyzstan",
    "currency_from": "GBP",
    "currency_to": "USD"
}

RSS_FEEDS = {
    "bbc": "http://feeds.bbci.co.uk/news/rss.xml",
    "cnn": "http://rss.cnn.com/rss/edition.rss",
    "fox": "http://feeds.foxnews.com/foxnews/latest",
    "iol": "http://www.iol.co.za/cmlink/1.640"
}

WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=d86c7af8adfa59f425d67ff62f06990a"
CURRENCY_API_URL = "https://openexchangerates.org//api/latest.json?app_id=1d17d94d9a3442a3b446e6d3533b0413"

@app.route("/")
def home():
    publication = request.args.get("publication")

    if not publication or publication.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    
    articles = get_news(publication)

    city = request.args.get("city")

    if not city:
        city = DEFAULTS["city"]

    weather = get_weather(city)

    currency_from = request.args.get("currency_from", default=DEFAULTS["currency_from"])
    currency_to = request.args.get("currency_to", default=DEFAULTS["currency_to"])

    rate, currencies = get_rate(currency_from, currency_to)

    return render_template("home.html",
                            articles=articles,
                            weather=weather,
                            currency_from=currency_from,
                            currency_to=currency_to,
                            rate=rate,
                            currencies=sorted(currencies))

def get_news(publication):
    if not publication or publication.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]

    feed = feedparser.parse(RSS_FEEDS[publication.lower()])

    return feed["entries"]

def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_API_URL.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None

    if parsed.get("weather"):
        weather = {
            "description": parsed["weather"][0]["description"],
            "temperature": parsed["main"]["temp"],
            "city": parsed["name"],
            "country": parsed["sys"]["country"]
        }
    
    return weather

def get_rate(frm, to):
    all_currency = urllib.request.urlopen(CURRENCY_API_URL).read()
    parsed = json.loads(all_currency).get("rates")
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())

    return (to_rate / frm_rate, parsed.keys())

if __name__ == "__main__":
    app.run(port=5000, debug=True)