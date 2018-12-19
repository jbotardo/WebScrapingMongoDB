from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
# client = pymongo.MongoClient(conn)

@app.route("/")
def index():
    mars_data_scrape = mongo.db.collection.find_one()
    
    return render_template("index.html", mars_data = mars_data_scrape)

@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data_scrape
    mars_data_get = scrape_mars.scrape()
    mars_data.update({}, mars_data_get, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)