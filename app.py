from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

# To create an instance of Flask
app = Flask(__name__)

# To setup mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# To route to render index.html template using data from Mongo
@app.route("/")
def home():

    # To find one record of data from the mongo database
    mars_data = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # To initiate MongoDB
    mars = mongo.db.mars
    
    # Run the scrape function to the mission to mars.py file -> to the function scrape
    mars_data = mission_to_mars.scrape_all()

    # Update the Mongo database using update and upsert=True
    # This update function is storing the data into the database
    mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
