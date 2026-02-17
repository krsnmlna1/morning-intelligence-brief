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

    def fetch_hackernews_top(self, limit=60) -> List[Dict]:
        """Fetch top stories from HackerNews"""
        try:
            response = requests.get(
                "https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10
            )
            story_ids = response.json()[:limit * 2]

            stories = []
            for story_id in story_ids:
                if len(stories) >= limit:
                    break
                story_response = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=10
                )
                story_data = story_response.json()
                if story_data and story_data.get('type') == 'story' and story_data.get('title'):
                    # NOTE: HackerNews items must NOT have 'subreddit' field
                    stories.append({
                        'title': story_data.get('title', ''),
                        'url': story_data.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                        'score': story_data.get('score', 0),
                        'comments': story_data.get('descendants', 0),
                        'source': 'HackerNews'
                    })
            return stories
        except Exception as e:
            print(f"Error fetching HackerNews: {e}")
            return []

    def filter_by_keywords(self, pool: List[Dict], keywords: List[str], limit=8) -> List[Dict]:
        """Filter stories from pool by keywords in title"""
        result = []
        for story in pool:
            title_lower = story.get('title', '').lower()
            if any(kw.lower() in title_lower for kw in keywords):
                result.append(story)
            if len(result) >= limit:
                break
        return result

    def fetch_reddit_hot(self, subreddit: str, limit=8) -> List[Dict]:
        """Fetch hot posts from a subreddit"""
        try:
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit + 3}&raw_json=1"
            response = requests.get(url, headers=self.reddit_headers, timeout=15)

            if response.status_code == 429:
                time.sleep(3)
                response = requests.get(url, headers=self.reddit_headers, timeout=15)

            if response.status_code != 200:
                print(f"Reddit r/{subreddit} → HTTP {response.status_code}")
                return []

            posts = []
            for post in response.json().get('data', {}).get('children', []):
                pd = post.get('data', {})
                if pd.get('stickied'):
                    continue
                posts.append({
                    'title': pd.get('title', ''),
                    'url': f"https://reddit.com{pd.get('permalink', '')}",
                    'score': pd.get('score', 0),
                    'comments': pd.get('num_comments', 0),
                    'subreddit': subreddit,
                    'source': f'r/{subreddit}'
                })
                if len(posts) >= limit:
                    break

            time.sleep(0.5)
            return posts
        except Exception as e:
            print(f"Error fetching r/{subreddit}: {e}")
            return []

    def fetch_github_trending(self, language: str = '', topic: str = '') -> List[Dict]:
        """Fetch trending GitHub repos"""
        try:
            week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            query = f"created:>{week_ago} stars:>20"
            if language:
                query += f" language:{language}"
            if topic:
                query += f" topic:{topic}"

            params = {'q': query, 'sort': 'stars', 'order': 'desc', 'per_page': 5}
            response = requests.get(
                "https://api.github.com/search/repositories",
                headers=self.headers, params=params, timeout=10
            )
            if response.status_code != 200:
                return []

            repos = []
            for repo in response.json().get('items', []):
                repos.append({
                    'name': repo.get('full_name', ''),
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

    def fetch_news_api(self, query: str = '', category: str = '') -> List[Dict]:
        """Fetch from NewsAPI (optional)"""
        if not self.news_api_key:
            return []
        try:
            if category:
                url = "https://newsapi.org/v2/top-headlines"
                params = {'apiKey': self.news_api_key, 'category': category, 'language': 'en', 'pageSize': 6}
            else:
                yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                url = "https://newsapi.org/v2/everything"
                params = {'apiKey': self.news_api_key, 'q': query, 'from': yesterday,
                          'sortBy': 'popularity', 'language': 'en', 'pageSize': 6}

            response = requests.get(url, params=params, timeout=10)
            articles = []
            for a in response.json().get('articles', []):
                if a.get('title') and '[Removed]' not in a.get('title', ''):
                    articles.append({
                        'title': a.get('title', ''),
                        'url': a.get('url', ''),
                        'score': 500,  # High but consistent score for NewsAPI
                        'comments': 0,
                        'source': a.get('source', {}).get('name', 'News')
                    })
            return articles
        except Exception as e:
            print(f"NewsAPI error: {e}")
            return []

    def collect_all_data(self) -> Dict[str, Any]:
        """Collect data from all sources"""
        print("🔍 Collecting intelligence data...")

        # ── Step 1: Fetch HackerNews pool once ──────────────────────────────
        print("  📰 HackerNews (60 stories)...")
        hn = self.fetch_hackernews_top(60)

        # ── Keyword lists ────────────────────────────────────────────────────
        AI_KW = [
            'ai', 'llm', 'gpt', 'openai', 'claude', 'anthropic', 'gemini',
            'mistral', 'ollama', 'transformer', 'neural network', 'machine learning',
            'deep learning', 'chatgpt', 'copilot', 'llama', 'hugging face',
            'langchain', 'deepseek', 'qwen', 'rag'
        ]
        STARTUP_KW = [
            'startup', 'we launched', 'show hn:', 'just launched', 'new tool',
            'funding', 'raises $', 'series a', 'series b', 'seed round',
            'y combinator', 'yc ', 'acquired', 'ipo', 'saas', 'mrr', 'arr',
            'bootstrapped', 'founder', 'side project', 'open source alternative',
        ]
        JOB_KW = [
            'who is hiring', 'seeking work', 'available for hire', 'remote position',
            'founding engineer', 'hiring engineer', 'hiring developer',
            'looking for engineer', 'looking for developer', 'we are hiring',
            'join our team'
        ]
        WORLD_KW = [
            'china', 'russia', 'ukraine', 'war', 'election', 'government',
            'policy', 'regulation', 'economy', 'tariff', 'sanction', 'climate',
            'nuclear', 'pentagon', 'congress', 'nato', 'geopolit', 'international'
        ]

        # ── Step 2: Build sections ───────────────────────────────────────────
        data = {
            'timestamp': datetime.now().isoformat(),
            'tech_news': {
                'hackernews_top': hn[:10],
            },
            'ai_ml': {
                'hackernews_ai': self.filter_by_keywords(hn, AI_KW, 8),
                'github_python': self.fetch_github_trending('python'),
                'github_ai_topic': self.fetch_github_trending(topic='machine-learning'),
            },
            'startups': {
                'hackernews_startup': self.filter_by_keywords(hn, STARTUP_KW, 6),
            },
            'remote_jobs': {
                'hackernews_jobs': self.filter_by_keywords(hn, JOB_KW, 6),
            },
            'world_news': {
                'hackernews_world': self.filter_by_keywords(hn, WORLD_KW, 8),
            }
        }

        # ── Step 3: Reddit (bonus, skip if blocked) ──────────────────────────
        print("  🔴 Reddit...")
        reddit_map = [
            ('ai_ml',       'r_machinelearning', 'MachineLearning',  6),
            ('ai_ml',       'r_localllama',      'LocalLLaMA',       5),
            ('startups',    'r_startups',        'startups',         5),
            ('remote_jobs', 'r_remotework',      'remotework',       5),
            ('remote_jobs', 'r_forhire',         'forhire',          5),
            ('remote_jobs', 'r_digitalnomad',    'digitalnomad',     5),
            ('world_news',  'r_worldnews',       'worldnews',        6),
            ('world_news',  'r_geopolitics',     'geopolitics',      4),
        ]
        for cat, key, sub, lim in reddit_map:
            posts = self.fetch_reddit_hot(sub, lim)
            if posts:
                data[cat][key] = posts
                print(f"    ✅ r/{sub}: {len(posts)}")
            else:
                print(f"    ⚠️  r/{sub}: skipped")

        # ── Step 4: NewsAPI (optional) ───────────────────────────────────────
        # NewsAPI removed from ai_ml and world_news sections per requirements
        # Can add back for other sections if needed

        print("✅ Collection complete!")
        return data


def main():
    scraper = IntelligenceScraper()
    data = scraper.collect_all_data()
    os.makedirs('data', exist_ok=True)
    with open('data/raw_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("📁 Saved to data/raw_data.json")


if __name__ == "__main__":
    main()
