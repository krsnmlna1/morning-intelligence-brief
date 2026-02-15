#!/usr/bin/env python3
"""
Morning Intelligence Brief - Data Scraper
Fetches news, tech updates, AI/ML developments, startup news, and market data
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os

class IntelligenceScraper:
    def __init__(self):
        self.news_api_key = os.getenv('NEWS_API_KEY', '')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def fetch_hackernews_top(self, limit=10) -> List[Dict]:
        """Fetch top stories from HackerNews"""
        try:
            # Get top story IDs
            top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = requests.get(top_stories_url, timeout=10)
            story_ids = response.json()[:limit]
            
            stories = []
            for story_id in story_ids:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_response = requests.get(story_url, timeout=10)
                story_data = story_response.json()
                
                if story_data and story_data.get('type') == 'story':
                    stories.append({
                        'title': story_data.get('title', 'No title'),
                        'url': story_data.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                        'score': story_data.get('score', 0),
                        'comments': story_data.get('descendants', 0)
                    })
            
            return stories
        except Exception as e:
            print(f"Error fetching HackerNews: {e}")
            return []
    
    def fetch_reddit_hot(self, subreddit: str, limit=5) -> List[Dict]:
        """Fetch hot posts from a subreddit"""
        try:
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.json()
            
            posts = []
            for post in data.get('data', {}).get('children', []):
                post_data = post.get('data', {})
                posts.append({
                    'title': post_data.get('title', 'No title'),
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'score': post_data.get('score', 0),
                    'comments': post_data.get('num_comments', 0),
                    'subreddit': subreddit
                })
            
            return posts
        except Exception as e:
            print(f"Error fetching Reddit r/{subreddit}: {e}")
            return []
    
    def fetch_news_api(self, query: str, category: str = None) -> List[Dict]:
        """Fetch news from NewsAPI"""
        if not self.news_api_key:
            return []
        
        try:
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            if category:
                url = f"https://newsapi.org/v2/top-headlines"
                params = {
                    'apiKey': self.news_api_key,
                    'category': category,
                    'language': 'en',
                    'pageSize': 5
                }
            else:
                url = f"https://newsapi.org/v2/everything"
                params = {
                    'apiKey': self.news_api_key,
                    'q': query,
                    'from': yesterday,
                    'sortBy': 'popularity',
                    'language': 'en',
                    'pageSize': 5
                }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            articles = []
            for article in data.get('articles', []):
                articles.append({
                    'title': article.get('title', 'No title'),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'description': article.get('description', '')
                })
            
            return articles
        except Exception as e:
            print(f"Error fetching NewsAPI for {query}: {e}")
            return []
    
    def fetch_github_trending(self, language: str = '') -> List[Dict]:
        """Fetch trending repos from GitHub"""
        try:
            url = "https://api.github.com/search/repositories"
            yesterday = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            query = f"created:>{yesterday}"
            if language:
                query += f" language:{language}"
            
            params = {
                'q': query,
                'sort': 'stars',
                'order': 'desc',
                'per_page': 5
            }
            
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.json()
            
            repos = []
            for repo in data.get('items', []):
                repos.append({
                    'name': repo.get('full_name', 'Unknown'),
                    'description': repo.get('description', 'No description'),
                    'url': repo.get('html_url', ''),
                    'stars': repo.get('stargazers_count', 0),
                    'language': repo.get('language', 'Unknown')
                })
            
            return repos
        except Exception as e:
            print(f"Error fetching GitHub trending: {e}")
            return []
    
    def collect_all_data(self) -> Dict[str, Any]:
        """Collect data from all sources"""
        print("🔍 Collecting intelligence data...")
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'tech_news': {
                'hackernews': self.fetch_hackernews_top(10),
                'reddit_programming': self.fetch_reddit_hot('programming', 5),
                'reddit_technology': self.fetch_reddit_hot('technology', 5),
            },
            'ai_ml': {
                'reddit_machinelearning': self.fetch_reddit_hot('MachineLearning', 5),
                'reddit_localllama': self.fetch_reddit_hot('LocalLLaMA', 5),
                'github_trending': self.fetch_github_trending('python'),
            },
            'startups': {
                'reddit_startups': self.fetch_reddit_hot('startups', 5),
                'reddit_entrepreneur': self.fetch_reddit_hot('Entrepreneur', 3),
            },
            'remote_jobs': {
                'reddit_remotejobs': self.fetch_reddit_hot('remotejs', 5),
                'reddit_forhire': self.fetch_reddit_hot('forhire', 5),
            },
            'world_news': {
                'reddit_worldnews': self.fetch_reddit_hot('worldnews', 5),
            }
        }
        
        # Add NewsAPI data if available
        if self.news_api_key:
            data['news_api'] = {
                'tech': self.fetch_news_api('technology OR artificial intelligence', 'technology'),
                'business': self.fetch_news_api('', 'business'),
            }
        
        print("✅ Data collection complete!")
        return data

def main():
    scraper = IntelligenceScraper()
    data = scraper.collect_all_data()
    
    # Save to JSON file
    output_file = 'data/raw_data.json'
    os.makedirs('data', exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"📁 Data saved to {output_file}")
    print(f"📊 Total items collected: {sum(len(v) if isinstance(v, list) else sum(len(vv) if isinstance(vv, list) else 0 for vv in v.values()) for v in data.values() if isinstance(v, (list, dict)))}")

if __name__ == "__main__":
    main()
