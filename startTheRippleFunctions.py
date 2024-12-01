# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

# API key for NewsAPI
API_KEY = os.getenv("API_KEY") 
url = 'https://newsapi.org/v2/everything'

# YouTube API credentials
YT_API_KEY = os.getenv("YT_API_KEY")
YT_url = "https://www.googleapis.com/youtube/v3/search"

# used for doing API calls
import requests

# for better formatting the publishing times of articles and videos
from datetime import datetime

# used for automatic and manual generated YT transcripts
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

# used with unescape to remove HTML special characters like &#39 for '
import html

# Used to determine the language of a description
from langdetect import detect, LangDetectException

# Used for getting daily quotes
from quotes_library import get_quotes, get_authors, get_categories

# for summarizing scripts
from summarizer import summarize_transcript

# used for Ripple Counter Shares
import random 


# returns a random subject word to help with variety on the homepage video
def random_subject():
    words = ['cat', 'dog', 'squirrel']

    random_word = random.choice(words)

    return random_word

# return a random number of shares
def shares_today():
    return random.randrange(5,50)

# get random inspiration quotes
def quote_of_the_day():
    getquote = get_quotes(category='inspirational', count=1, random = True)

    # get the quote from the quote of the day dictionary
    quote = getquote['data'][0]['quote']

    # get the author from the quote of the day dictionary
    author = getquote['data'][0]['author']

    # set as a list and return the list
    quote_list = [author, quote]
    return quote_list

#print(quote_of_the_day()['data'][0]['quote'])

"""Fetches articles using NewsAPI"""
def fetch_articles_with_cache(niche):

    websites = {'Tech':['techcrunch.com','goodnewsnetwork.org','spectrum.ieee.org','springwise.com'],
            'Health': ['goodnewsnetwork.org','medicalnewstoday.com','positive.news','sciencedaily.com'],
            'Science':['newscientist.com','sciencedaily.com','nasa.gov','goodnewsnetwork.org'],
            'Education':['goodnewsnetwork.org','bbc.com ','positive.news','edutopia.org']
}
    # print("Fetching data from NewsAPI")

    # add all the websites together for but only for each category
    domains = ",".join(websites[niche])

    # Define parameters
    params = {
        'q': f'{niche} AND (innovation OR "positive impact" OR inspire) NOT (Trump OR politics OR Harris OR Biden)',
        'domains': domains, # the websites queried
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 10, # limit to 5 results
        'apiKey': API_KEY
    }

    #print(params)
    # Get the requested parameters from the URL
    response = requests.get(url, params=params)
   
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        # Print to the screen the status code error
        print(f"API Error: {response.status_code}")
        return []


def date_format(timestamp):

    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    # format the timestamp to Month-Day-Year format
    formatted_date = dt.strftime("%B-%d-%Y")

    return formatted_date


# determines if a video has a transcript or if they are disabled
def is_there_a_transcript(video_Id):
    try: # get the transcript from the Video
        transcript = YouTubeTranscriptApi.get_transcript(video_Id)

    except NoTranscriptFound:
        print("No transcript found for the videoId: ", video_Id)
        return False
    
    except TranscriptsDisabled:
        print("Transcripts are disabled for the videoId: ", video_Id)
        return False

    # if video has a transcript
    return True


def fetch_youtube_videos(query):
    params = {
        "part": "snippet",  # Basic metadata: title, description, etc.
        "q": query,         # Search term
        "type": "video",    # Only fetch videos
        "order": "date",    # Order results by upload date (reverse order/most recent first)
        "maxResults": 10,   # Limit results to 10 videos
        "relevanceLanguage": "en",  # Prioritize English results
        "key": YT_API_KEY
    }

    # use reponse to get params from YT API
    response = requests.get(YT_url, params=params)
    if response.status_code == 200:
        videos = response.json().get("items", [])

        # go through each video to determine if it's in English
        filtered_videos = []
        for video in videos:
            title = video['snippet']['title']
            description = video['snippet']['description']
            videoId = video['id']['videoId']

            # check if there is a transcript in the first place
            if is_there_a_transcript(videoId):

                # look and see if the title and description are in English
                try:
                    if detect(title) == 'en' and detect(description) == 'en':
                        filtered_videos.append(video) # if so, add to list

                except LangDetectException:
                    print("Language Detection Failed for: ", title, description)


        # convert HTML special characters
        for video in filtered_videos:
            video['snippet']['title'] = html.unescape(video['snippet']['title'])
        return filtered_videos

    else:
        print(f"API Error: {response.status_code}")
        return []

def fetch_youtube_videos_for_homepage(query):
    params = {
        "part": "snippet",  # Basic metadata: title, description, etc.
        "q": query,         # Search term
        "type": "video",    # Only fetch videos
        "order": "date",    # Order results by upload date (reverse order/most recent first)
        "maxResults": 10,   # Limit results to 10 videos
        "relevanceLanguage": "en",  # Prioritize English results
        "key": YT_API_KEY
    }

    # use reponse to get params from YT API
    response = requests.get(YT_url, params=params)
    if response.status_code == 200:
        videos = response.json().get("items", [])

        # convert HTML special characters
        for video in videos:
            video['snippet']['title'] = html.unescape(video['snippet']['title'])
        return videos

    else:
        print(f"API Error: {response.status_code}")
        return []

# Gets the transcript from a YouTube Video
def YouTube_Transcript(video_Id):

    # get the transcript from the Video
    transcript = YouTubeTranscriptApi.get_transcript(video_Id)

    if transcript:

        # get each word from the transcript
        listed_words_transcript = []
        for entry in transcript:
            text = entry['text']
            words = text.split()
            listed_words_transcript.extend(words)

        # join all the words together for 1 coherent transcript
        formatted_transcript = " ".join(listed_words_transcript)

        # get the summary of the formatted transcript
        summary = summarize_transcript(formatted_transcript)
        #print(summary)
        # return the summary
        return summary

    return "There is no transcript for this video."
