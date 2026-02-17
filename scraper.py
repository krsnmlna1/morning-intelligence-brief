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
import time

class IntelligenceScraper:
    def __init__(self):
        self.news_api_key = os.getenv('NEWS_API_KEY', '')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.reddit_headers = {
            'User-Agent': 'MorningBrief/1.0 (by /u/morningbrief_bot)',
            'Accept': 'application/json',
        }

    def fetch_hackernews_top(self, limit=10) -> List[Dict]:
        """Fetch top stories from HackerNews"""
        try:
            top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = requests.get(top_stories_url, timeout=10)
            story_ids = response.json()[:limit * 2]  # Fetch more in case some are not stories

            stories = []
            for story_id in story_ids:
                if len(stories) >= limit:
                    break
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_response = requests.get(story_url, timeout=10)
                story_data = story_response.json()

                if story_data and story_data.get('type') == 'story' and story_data.get('url'):
                    stories.append({
                        'title': story_data.get('title', 'No title'),
                        'url': story_data.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                        'score': story_data.get('score', 0),
                        'comments': story_data.get('descendants', 0),
                        'source': 'HackerNews'
                    })

            return stories
        except Exception as e:
            print(f"Error fetching HackerNews: {e}")
            return []

    def fetch_hackernews_category(self, keywords: List[str], limit=5) -> List[Dict]:
        """Fetch HackerNews stories filtered by keywords"""
        try:
            all_stories = self.fetch_hackernews_top(30)
            filtered = []
            for story in all_stories:
                title_lower = story['title'].lower()
                if any(kw.lower() in title_lower for kw in keywords):
                    filtered.append(story)
                if len(filtered) >= limit:
                    break
            return filtered
        except Exception as e:
            print(f"Error filtering HackerNews: {e}")
            return []

    def fetch_reddit_hot(self, subreddit: str, limit=5) -> List[Dict]:
        """Fetch hot posts from a subreddit"""
        try:
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}&raw_json=1"
            response = requests.get(url, headers=self.reddit_headers, timeout=15)

            if response.status_code == 429:
                print(f"Reddit rate limited for r/{subreddit}, waiting...")
                time.sleep(2)
                response = requests.get(url, headers=self.reddit_headers, timeout=15)

            if response.status_code != 200:
                print(f"Reddit r/{subreddit} returned status {response.status_code}")
                return []

            data = response.json()
            posts = []
            for post in data.get('data', {}).get('children', []):
                post_data = post.get('data', {})
                # Skip stickied/pinned posts
                if post_data.get('stickied', False):
                    continue
                posts.append({
                    'title': post_data.get('title', 'No title'),
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'score': post_data.get('score', 0),
                    'comments': post_data.get('num_comments', 0),
                    'subreddit': subreddit,
                    'source': f'r/{subreddit}'
                })

            time.sleep(0.5)  # Be polite to Reddit
            return posts
        except Exception as e:
            print(f"Error fetching Reddit r/{subreddit}: {e}")
            return []

    def fetch_github_trending(self, language: str = '') -> List[Dict]:
        """Fetch trending repos from GitHub - FIXED: params now properly passed"""
        try:
            url = "https://api.github.com/search/repositories"
            week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

            query = f"created:>{week_ago} stars:>10"
            if language:
                query += f" language:{language}"

            params = {
                'q': query,
                'sort': 'stars',
                'order': 'desc',
                'per_page': 5
            }

            # FIX: params now correctly passed to requests.get
            response = requests.get(url, headers=self.headers, params=params, timeout=10)

            if response.status_code != 200:
                print(f"GitHub API returned status {response.status_code}")
                return []

            data = response.json()
            repos = []
            for repo in data.get('items', []):
                repos.append({
                    'name': repo.get('full_name', 'Unknown'),
                    'description': repo.get('description', 'No description') or 'No description',
                    'url': repo.get('html_url', ''),
                    'stars': repo.get('stargazers_count', 0),
                    'language': repo.get('language', 'Unknown') or 'Unknown',
                    'source': 'GitHub'
                })

            return repos
        except Exception as e:
            print(f"Error fetching GitHub trending: {e}")
            return []

    def fetch_dev_to(self, tag: str = '', limit=5) -> List[Dict]:
        """Fetch articles from dev.to (free, no auth needed)"""
        try:
            url = "https://dev.to/api/articles"
            params = {
                'per_page': limit,
                'top': 1,  # top articles
            }
            if tag:
                params['tag'] = tag

            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            if response.status_code != 200:
                return []

            articles = []
            for article in response.json():
                articles.append({
                    'title': article.get('title', 'No title'),
                    'url': article.get('url', ''),
                    'score': article.get('public_reactions_count', 0),
                    'comments': article.get('comments_count', 0),
                    'source': 'dev.to'
                })
            return articles
        except Exception as e:
            print(f"Error fetching dev.to tag={tag}: {e}")
            return []

    def fetch_news_api(self, query: str, category: str = None) -> List[Dict]:
        """Fetch news from NewsAPI"""
        if not self.news_api_key:
            return []

        try:
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

            if category:
                url = "https://newsapi.org/v2/top-headlines"
                params = {
                    'apiKey': self.news_api_key,
                    'category': category,
                    'language': 'en',
                    'pageSize': 5
                }
            else:
                url = "https://newsapi.org/v2/everything"
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
                if article.get('title') and '[Removed]' not in article.get('title', ''):
                    articles.append({
                        'title': article.get('title', 'No title'),
                        'url': article.get('url', ''),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'description': article.get('description', ''),
                        'score': 100,  # NewsAPI articles get high default score
                    })

            return articles
        except Exception as e:
            print(f"Error fetching NewsAPI for {query}: {e}")
            return []

    def collect_all_data(self) -> Dict[str, Any]:
        """Collect data from all sources"""
        print("🔍 Collecting intelligence data...")

        # Fetch HackerNews once, reuse for filtering
        print("  📰 Fetching HackerNews...")
        hn_all = self.fetch_hackernews_top(30)

        print("  🤖 Fetching AI/ML data...")
        data = {
            'timestamp': datetime.now().isoformat(),
            'tech_news': {
                'hackernews': hn_all[:10],
                'devto_webdev': self.fetch_dev_to('webdev', 5),
                'devto_programming': self.fetch_dev_to('programming', 5),
            },
            'ai_ml': {
                'hackernews_ai': self.fetch_hackernews_category(
                    ['AI', 'GPT', 'LLM', 'machine learning', 'neural', 'OpenAI', 'Claude', 'Anthropic', 'Gemini', 'artificial intelligence', 'deep learning'], 5
                ),
                'devto_ai': self.fetch_dev_to('ai', 5),
                'github_trending_python': self.fetch_github_trending('python'),
                'github_trending_ai': self.fetch_github_trending(''),
            },
            'startups': {
                'hackernews_startup': self.fetch_hackernews_category(
                    ['startup', 'launch', 'funding', 'raises', 'YC', 'seed', 'series', 'acquired', 'IPO'], 5
                ),
                'devto_career': self.fetch_dev_to('career', 3),
            },
            'remote_jobs': {
                'hackernews_jobs': self.fetch_hackernews_category(
                    ['hiring', 'job', 'remote', 'engineer', 'developer', 'freelance', 'work from home'], 5
                ),
                'devto_career': self.fetch_dev_to('career', 5),
            },
            'world_news': {
                'hackernews_news': self.fetch_hackernews_category(
                    ['policy', 'government', 'economy', 'climate', 'regulation', 'law', 'geopolitic', 'war', 'election', 'global'], 5
                ),
            }
        }

        print("  🔴 Fetching Reddit (may be slow)...")
        # Reddit as bonus - add if available, skip if blocked
        reddit_sources = [
            ('ai_ml', 'reddit_machinelearning', 'MachineLearning', 5),
            ('ai_ml', 'reddit_localllama', 'LocalLLaMA', 5),
            ('startups', 'reddit_startups', 'startups', 5),
            ('remote_jobs', 'reddit_remotejobs', 'remotejobs', 5),
            ('world_news', 'reddit_worldnews', 'worldnews', 5),
        ]

        for category, key, subreddit, limit in reddit_sources:
            posts = self.fetch_reddit_hot(subreddit, limit)
            if posts:
                data[category][key] = posts
                print(f"    ✅ r/{subreddit}: {len(posts)} posts")
            else:
                print(f"    ⚠️  r/{subreddit}: no data (skipped)")

        # Add NewsAPI if key available
        if self.news_api_key:
            print("  📡 Fetching NewsAPI...")
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
