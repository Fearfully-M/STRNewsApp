import os 
from flask import Flask, flash, redirect, render_template, request, session, jsonify

from flask_session import Session

from startTheRippleFunctions import (
    fetch_youtube_videos_for_homepage, 
    random_subject, shares_today, quote_of_the_day, 
    fetch_youtube_videos, fetch_articles_with_cache, 
    date_format, YouTube_Transcript, )

import json

# Configure application
app = Flask(__name__)

# the idea to simply cache like this was inspired by ChatGPT
# my original idea was much more complicated and involved Python caching libraries that ended up
# not being necessary for this project

# In-memory cache to store articles for each category
category_cache = {}

# In-memory cache to store videos for each category
YouTube_category_cache = {}

# In-memory cache to store the homePage Video
homepageVideo_Cache = {}

# Custom filter
app.jinja_env.filters["date_format"] = date_format
app.jinja_env.filters["YouTube_Transcript"] = YouTube_Transcript

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# CSS class for active page on the navbar
NAV_ACTIVE = "active"

# get the shares today and the quote of the day
SHARES = shares_today()
QUOTE = quote_of_the_day()

@app.route("/", methods=["GET", "POST"])
def home():
    """Main Home Page to get User's Niche Choice"""

    # this ended up being a bug I couldn't figure out without prompting ChatGPT
    global homepageVideo_Cache # use the variable of the outer scope (out of home def) variable instead

    # get a homepageVideo if it doesn't exist  
    if not homepageVideo_Cache:
        # get a random subject
        subject = random_subject()
        print(f"Fetching a {subject} video for Home Page")

        # fetch a funny video with the random subject for the homepage
        query = "funny " + subject
        homepageVideo = fetch_youtube_videos_for_homepage(query)

        # If there is no description for the video then set one
        if homepageVideo[0]['snippet']['description'] == "":
            homepageVideo[0]['snippet']['description'] = "No YouTube Video Description Available."

        # store the video into the homepageVideo_Cache
        homepageVideo_Cache = homepageVideo


    # If there is a homepageVideo get it from cache to avoid the YT API Call
    elif homepageVideo_Cache:
        print("Loading cached Home Page Video")
        homepageVideo = homepageVideo_Cache

    elif not homepageVideo_Cache and not homepageVideo:
        #Return an error if no category is specified
        return jsonify({"error": "No category specified"}), 400


    return render_template("layout.html", quote = QUOTE, shares = SHARES, homepageVideo = homepageVideo, NAV_ACTIVE = NAV_ACTIVE)

# this '/' will need to be worked on to change based on user picked niche
@app.route("/niche", methods=["GET", "POST"])
def get_niche():
    """Generate Positive News Based on the Niche the user selected"""
    # Get the 'category' parameter from the query string
    category = request.args.get('category', None)

    if category:
        # Check if the cateogry is already cached
        if category in category_cache:
            # Fetch articles only for the selected category
            print(f"Loading cached data for {category}")
            articles = category_cache[category]
        else:
            print(f"Fetching data for {category} from NewsAPI...")
            articles = fetch_articles_with_cache(category)
            if articles: # Cache only if the data is valid
                category_cache[category] = articles

        # Prepare the data for rendering
        niche = {"category": category, "news": articles}

        # Debugging: Print the first article's title, if it exists
        # if articles:
            # print(niche['news'][0]['title'])
            # pretty_json = json.dumps(niche, indent=4)
            # print(pretty_json)

        # Render the template with the niche data
        return render_template("niche.html", niche = niche, shares = SHARES, NAV_ACTIVE = NAV_ACTIVE)
    else:
        # Return an error if no category is specified
        return jsonify({"error": "No category specified"}), 400

# this '/' will need to be worked on to change based on user picked niche
@app.route("/YouTube", methods=["GET", "POST"])
def get_YouTube():

    if request.method == "GET":

        # Get the 'category' parameter from the query string
        category = request.args.get('category', None)

        # category was set to YouTube to get to this route
        # initialize category to None when user first clicks 'YouTube'
        if category == 'YouTube':
            category = None

    if category:
        # Create caching to ease up on YT API Calls 
        if category in YouTube_category_cache:
            # Use YouTube API to fetch 
            print(f"Loading cached data for {category}")
            videos = YouTube_category_cache[category]
        else:
            print(f"Fetching data for {category} from YouTube API...")
            query = category
            videos = fetch_youtube_videos(query)
            if videos: # Cache the data if API Call is valid
                YouTube_category_cache[category] = videos

        return render_template("YouTube.html", videos = videos, quote = QUOTE, shares = SHARES, NAV_ACTIVE = NAV_ACTIVE)

    else:
        # Return an error if no category is specified
        #return jsonify({"error": "No category specified"}), 400
        return render_template("YouTube.html", videos = None, quote = QUOTE, shares = SHARES, NAV_ACTIVE = NAV_ACTIVE)


if __name__ == '__main__':
    # Get the PORT from the environment variable, default to 5000 for local development
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
