#!/usr/bin/env python3
"""
Morning Intelligence Brief - AI Summarizer
Processes raw data and creates structured summaries
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Set


class IntelligenceSummarizer:
    def __init__(self, data_path='data/raw_data.json'):
        with open(data_path, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)
        self._used_titles: Set[str] = set()  # Global dedup tracker

    def extract_top_items(self, items: List[Dict], key='score', limit=5) -> List[Dict]:
        """Extract top items sorted by score, with global deduplication across sections"""
        if not items:
            return []
        sorted_items = sorted(items, key=lambda x: x.get(key, 0), reverse=True)

        result = []
        for item in sorted_items:
            # Filter out fake score 500 items (score >= 500 AND comments == 0)
            if item.get('score', 0) >= 500 and item.get('comments', 0) == 0:
                continue
            
            title = item.get('title', '').strip().lower()
            if not title or title in self._used_titles:
                continue
            self._used_titles.add(title)
            # Fix ugly "r/N/A" label for non-Reddit sources
            if item.get('subreddit') in ('N/A', '', None):
                item.pop('subreddit', None)
            result.append(item)
            if len(result) >= limit:
                break
        return result

    def flatten_section(self, section_data: dict, exclude_keys: List[str] = None) -> List[Dict]:
        """Flatten all lists from a section dict into one combined list"""
        combined = []
        for key, value in section_data.items():
            if isinstance(value, list):
                if exclude_keys and any(k in key for k in exclude_keys):
                    continue
                combined.extend(value)
        return combined

    def summarize_tech_news(self) -> Dict[str, Any]:
        tech_data = self.raw_data.get('tech_news', {})
        all_tech = self.flatten_section(tech_data)
        top_tech = self.extract_top_items(all_tech, 'score', 8)
        return {
            'title': '💻 Tech & Development',
            'items': top_tech,
            'summary': f"{len(top_tech)} trending topics in tech today"
        }

    def summarize_ai_ml(self) -> Dict[str, Any]:
        ai_data = self.raw_data.get('ai_ml', {})
        github_repos, discussions = [], []
        for key, value in ai_data.items():
            if isinstance(value, list):
                (github_repos if 'github' in key else discussions).extend(value)
        top_ai = self.extract_top_items(discussions, 'score', 6)
        top_repos = sorted(github_repos, key=lambda x: x.get('stars', 0), reverse=True)[:3]
        return {
            'title': '🤖 AI & Machine Learning',
            'discussions': top_ai,
            'trending_repos': top_repos,
            'summary': f"{len(top_ai)} AI discussions + {len(top_repos)} trending repos"
        }

    def summarize_startups(self) -> Dict[str, Any]:
        all_startups = self.flatten_section(self.raw_data.get('startups', {}))
        top = self.extract_top_items(all_startups, 'score', 5)
        return {'title': '🚀 Startups & Business', 'items': top, 'summary': f"{len(top)} insights from startup community"}

    def summarize_remote_jobs(self) -> Dict[str, Any]:
        all_jobs = self.flatten_section(self.raw_data.get('remote_jobs', {}))
        top = self.extract_top_items(all_jobs, 'score', 6)
        return {'title': '💼 Remote Opportunities', 'items': top, 'summary': f"{len(top)} remote job posts and discussions"}

    def summarize_world_news(self) -> Dict[str, Any]:
        all_news = self.flatten_section(self.raw_data.get('world_news', {}))
        top = self.extract_top_items(all_news, 'score', 6)
        return {'title': '🌍 World News', 'items': top, 'summary': f"{len(top)} important global updates"}

    def generate_summary(self) -> Dict[str, Any]:
        print("📝 Generating intelligence summary...")
        summary = {
            'date': datetime.now().strftime('%A, %B %d, %Y'),
            'time_generated': datetime.now().strftime('%H:%M WIB'),
            'sections': {
                'tech_news': self.summarize_tech_news(),
                'ai_ml': self.summarize_ai_ml(),
                'startups': self.summarize_startups(),
                'remote_jobs': self.summarize_remote_jobs(),
                'world_news': self.summarize_world_news(),
            },
            'insights': [
                "📈 Focus areas today: Stay updated on AI developments and remote opportunities",
                "🎯 Action items: Check trending GitHub repos for learning opportunities",
                "💡 Remember: Knowledge compounds - what you learn today builds tomorrow's advantage"
            ]
        }
        print("✅ Summary generated!")
        return summary

    def save_summary(self, summary: Dict[str, Any], output_path='data/summary.json'):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"💾 Summary saved to {output_path}")


def main():
    summarizer = IntelligenceSummarizer()
    summary = summarizer.generate_summary()
    summarizer.save_summary(summary)
    print("\n" + "="*50)
    print(f"📊 Intelligence Brief for {summary['date']}")
    print("="*50)
    for _, section_data in summary['sections'].items():
        print(f"\n{section_data['title']}\n  {section_data['summary']}")


if __name__ == "__main__":
    main()
