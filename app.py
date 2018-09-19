# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # # Run scraped functions
    news = scrape_mars.MarsNews()
    featureImage = scrape_mars.MarsSpaceImage()
    weather = scrape_mars.MarsWeather()
    marsFacts = scrape_mars.MarsFacts()
    marsHemi = scrape_mars.MarsHemi()

    # # Store results into a dictionary
    mars = {
        "news_title": news['Title'],
        "news_para": news['SubPara'],
        "mars_image": featureImage,
        "weather": weather,
        # "mars_facts": marsFacts,
        # "marsHemi": marsHemi
    }


    # Insert forecast into database
    mongo.db.collection.insert_one(mars)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
