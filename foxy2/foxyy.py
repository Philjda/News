
from flask import Flask, render_template, request
import feedparser
import requests
import sqlite3

app = Flask(__name__)
DB_PATH = "rss.db"


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

def store_articles(entries, publication):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for entry in entries:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        published = entry.get("published", "N/A")

        if not link or not title:
            continue  # ne pas insérer les articles incomplets

        c.execute("""
            INSERT OR IGNORE INTO articles (title, link, publication, published)
            VALUES (?, ?, ?, ?)
        """, (title, link, publication, published))

    conn.commit()
    conn.close()


@app.route("/")
def home():
    publication = request.args.get("publication") or "bbc"
    keyword = request.args.get("q", "").lower()

    feed_url = RSS_FEEDS.get(publication)
    feed = feedparser.parse(feed_url)
    entries = feed.entries

    # ✅ Stocker tous les articles dans la base
    store_articles(entries, publication)

    # 🔍 Si un mot-clé est fourni, on filtre les articles pour l'affichage
    if keyword:
        entries = [entry for entry in entries if keyword in entry.title.lower()]

    return render_template("home.html", articles=entries, publication=publication)


@app.route("/")
def get_news ():
	query = request.args.get("publication")
	if not query or query.lower() not in RSS_FEEDS:
		publication = 'rfi'
	else:
		publication = query.lower()
	feed = feedparser.parse(RSS_FEEDS[publication])
	return render_template("home.html", articles = feed['entries'])

@app.route("/stored")
def stored_articles():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT title, link, publication, published FROM articles ORDER BY stored_at DESC")
    results = c.fetchall()
    conn.close()
    return render_template("stored.html", articles=results)

@app.route("/search")
def search_articles():
    query = request.args.get("q", "").strip().lower()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if query:
        c.execute("""
            SELECT title, link, publication, published
            FROM articles
            WHERE LOWER(title) LIKE ?
            ORDER BY stored_at DESC
        """, ('%' + query + '%',))
        results = c.fetchall()
    else:
        results = []

    conn.close()
    return render_template("search.html", articles=results, query=query)


import csv
from flask import Response

@app.route("/export")
def export_articles():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT title, link, publication, published FROM articles ORDER BY stored_at DESC")
    rows = c.fetchall()
    conn.close()

    def generate():
        yield "title,link,publication,published\n"
        for row in rows:
            # Attention aux virgules dans les titres — les quotes sont nécessaires
            yield '"{}","{}","{}","{}"\n'.format(*[str(item).replace('"', '""') for item in row])

    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=articles.csv"})




	
if __name__ == '__main__':
	app.run(debug=True, use_reloader=False)