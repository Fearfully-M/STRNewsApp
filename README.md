# Positive News App - 'Start The Ripple'
#### Video Demo:  <URL HERE>
#### Description:

# Positive News Application

This is a positive news application built with **Python**, **Flask**, **HTML**, **CSS**, **Jinja**, and multiple Python libraries and APIs. Its purpose is to deliver uplifting and inspiring news by aggregating articles and videos from various niches.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [APIs Used](#apis-used)
- [Challenges and Learning](#challenges-and-learning)
- [Installation](#installation)
- [Usage](#usage)
- [Limitations](#limitations)
- [Future Plans](#future-plans)

---

## Overview

The goal of this project was to create a web application that focuses on **positive news** across four key niches:
- **Technology**
- **Health**
- **Science**
- **Education**

Additionally, the project explores positive content on YouTube and summarizes it using AI. This was an ambitious project aimed at demystifying:
1. **API Integration**: Understanding how to work with APIs to fetch, process, and display data.
2. **Web Deployment**: Learning how to deploy a web application online.

---

## Features

1. **News Aggregation:**
   - Fetches articles from 4 websites across the niches of Technology, Health, Science, and Education using the **NewsAPI**.
   - Displays article titles and descriptions, with links to the original sources.

2. **YouTube Video Summaries:**
   - Fetches positive news videos in the same niches using the **YouTube API**.
   - Retrieves video transcripts via a transcript API.
   - Summarizes transcripts using the **Hugging Face Transformer API**.

3. **Clean and User-Friendly Design:**
   - Designed with **Figma** before implementation, emphasizing a polished and intuitive user experience.

---

## APIs Used

1. **NewsAPI**  
   - Fetches articles from major news outlets.  
   - Free tier limits to 4 niches to avoid costs.

2. **YouTube API**  
   - Retrieves videos based on niche-related keywords.  

3. **Transcript API**  
   - Fetches manually or auto-generated transcripts for YouTube videos.

4. **Hugging Face Transformer API**  
   - Summarizes video transcripts using the **BART** model.
   - Free tier limits tokenization to ~1000 tokens per request.

---

## Challenges and Learning

### Initial Challenges:
- Overcoming uncertainty about API integration and web hosting.
- Managing the scope of the project to ensure it was challenging but feasible.

### Key Learnings:
- **API Integration:** Learned to work with multiple APIs and process data for a real-world application.
- **Cache Management** Learned at a elementary level of how to cache the API results to reduce the number of API calls needed
- **Web Deployment:** Successfully hosted the project online, allowing external access to the application (Not meant for other uses as API costs are signicate outside of free tiers).
- **Design Tools:** Explored **Figma** for the first time, gaining insight into its value for front-end and UX design.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/positive-news-app.git
   cd positive-news-app
2. pip install -r requirements.txt
3. Set up API Keys:
- Obtain API kets for **NewsAPI**, **YouTube API**, and **Hugging Face**
- Add them to an .env file:

        NEWS_API_KEY=your_news_api_key
        YOUTUBE_API_KEY=your_youtube_api_key
        HUGGINGFACE_API_KEY=your_huggingface_api_key

## Usage

1. Visit the homepage to explore uplifting news from various niches.
2. Click on an article to read more on the original source.
3. Navigate to the YouTube page to find summarized videos.

## Limitations

Tokenization Limits:

    The free tier of Hugging Face's API limits summarization to ~1000 tokens (about 824 words per request). This affects summarization quality for long transcripts.

Performance:

    Using a cloud-based Hugging Face API results in slow loading times, especially on the YouTube page, where transcript summarization can take up to a minute.

## Future Plans

- Web Scraping: Incorporate web scraping for trending news stories.
- Trending News App: Streamline the application to focus on trending news rather than summarization, making it faster and more versatile.
- CLI Tool: Adapt the project into a command-line tool for personal use.

This project has been a significant learning experience, and I’m proud of what I’ve accomplished. Despite its limitations, it’s a functional application that tackles real-world challenges and demonstrates growth in API integration and deployment.