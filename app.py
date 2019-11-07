from flask import Flask, render_template, redirect
import pymongo
#from flask_pymongo import PyMongo
import scrape_mars1

#Flask app
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017/mars_app'
mongo = pymongo.MongoClient(conn)

#Flask to Mongo connection
@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", final_mars=final_mars)


@app.route("/scrape")
def scrape():
    
    mars_data = scrape_mars1.scrape_website()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)