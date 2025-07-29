
from flask import Flask, render_template, request
import feedparser
import requests

app = Flask(__name__)

RSS_FEEDS = {
	'bbc' : 'http://feeds.bbci.co.uk/news/rss.xml',
	'cnn' : 'http://rss.cnn.com/rss/edition.rss',
	'fox' : 'http://feeds.foxnews.com/foxnews/latest',
	'lepoint': 'https://www.lepoint.fr/24h-infos/rss.xml',
	'rfi' : 'http://www.rfi.fr/europe/rss',
	'frinfo': 'https://www.francetvinfo.fr/titres.rss',
	'europe': 'https://www.francetvinfo.fr/monde/europe.rss',
	'europ': 'https://www.touteleurope.eu/rss/tous-les-contenus.html',
	'euroeco' : 'https://www.economist.com/europe/rss.xml',
	'wired' : 'https://www.wired.com/feed/rss',
	'nyt': 'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml',
	'time' : 'http://feeds.feedburner.com/time/business',
	'eco' : 'https://www.economist.com/science-and-technology/rss.xml',
	'diplo': 'https://www.diploweb.com/spip.php?page=backend',
	'diplo2' : 'http://radiofrance-podcast.net/podcast09/rss_10009.xml',
	'youby': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCWWPKhD0fbAHHMg9_i6JQ5A',
	'youby2': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCYO_jab_esuFRV4b17AJtAw'
	}


@app.route("/")
def get_news ():
	query = request.args.get("publication")
	if not query or query.lower() not in RSS_FEEDS:
		publication = 'rfi'
	else:
		publication = query.lower()
	feed = feedparser.parse(RSS_FEEDS[publication])
	return render_template("home.html", articles = feed['entries'])
	
if __name__ == '__main__':
	app.run(debug=True, use_reloader=False)