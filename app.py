import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

class RedditSummarizer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.gemini_api_url = "https://gemini.api.url/summarize"  # Replace with the actual Gemini API endpoint
        self.gemini_api_key = "your_gemini_api_key"  # Replace with your Gemini API key

    def extract_reddit_content(self, url):
        """Extract content from Reddit post URL"""
        try:
            # Convert URL to JSON API URL
            if 'www.reddit.com' in url:
                url = url.replace('www.reddit.com', 'api.reddit.com')
            
            # Add .json to the URL if not present
            if not url.endswith('.json'):
                url = f"{url}.json"
            
            response = requests.get(url, headers=self.headers)
            data = response.json()
            
            # Extract post title and content
            post_data = data[0]['data']['children'][0]['data']
            title = post_data['title']
            content = post_data.get('selftext', '')
            
            return title, content
        except Exception as e:
            return None, f"Error extracting content: {str(e)}"

    def clean_text(self, text):
        """Clean the text by removing special characters and extra whitespace"""
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        # Remove Reddit formatting
        text = re.sub(r'.*?|.*?', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text

    def summarize_text(self, text, max_length=150, min_length=50):
        """Summarize text using Gemini API"""
        try:
            cleaned_text = self.clean_text(text)
            payload = {
                "text": cleaned_text,
                "max_length": max_length,
                "min_length": min_length
            }
            headers = {
                "Authorization": f"Bearer {self.gemini_api_key}",
                "Content-Type": "application/json"
            }
            response = requests.post(self.gemini_api_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                summary = response.json().get("summary", "")
                return summary
            else:
                return f"Error: Gemini API responded with status {response.status_code}: {response.text}"
        except Exception as e:
            return f"Error generating summary: {str(e)}"