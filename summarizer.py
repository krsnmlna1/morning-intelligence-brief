#!/usr/bin/env python3
"""
Morning Intelligence Brief - AI Summarizer
Processes raw data and creates structured summaries
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class IntelligenceSummarizer:
    def __init__(self, data_path='data/raw_data.json'):
        with open(data_path, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)
    
    def extract_top_items(self, items: List[Dict], key='score', limit=5) -> List[Dict]:
        """Extract top items sorted by a key"""
        if not items:
            return []
        sorted_items = sorted(items, key=lambda x: x.get(key, 0), reverse=True)
        return sorted_items[:limit]
    
    def summarize_tech_news(self) -> Dict[str, Any]:
        """Summarize tech news from multiple sources"""
        tech_data = self.raw_data.get('tech_news', {})
        
        # Combine and rank all tech news
        all_tech = []
        all_tech.extend(tech_data.get('hackernews', []))
        all_tech.extend(tech_data.get('reddit_programming', []))
        all_tech.extend(tech_data.get('reddit_technology', []))
        
        top_tech = self.extract_top_items(all_tech, 'score', 8)
        
        return {
            'title': '💻 Tech & Development',
            'items': top_tech,
            'summary': f"{len(top_tech)} trending topics in tech today"
        }
    
    def summarize_ai_ml(self) -> Dict[str, Any]:
        """Summarize AI/ML developments"""
        ai_data = self.raw_data.get('ai_ml', {})
        
        all_ai = []
        all_ai.extend(ai_data.get('reddit_machinelearning', []))
        all_ai.extend(ai_data.get('reddit_localllama', []))
        
        top_ai = self.extract_top_items(all_ai, 'score', 6)
        
        # Add GitHub trending
        github_repos = ai_data.get('github_trending', [])[:3]
        
        return {
            'title': '🤖 AI & Machine Learning',
            'discussions': top_ai,
            'trending_repos': github_repos,
            'summary': f"{len(top_ai)} AI discussions + {len(github_repos)} trending repos"
        }
    
    def summarize_startups(self) -> Dict[str, Any]:
        """Summarize startup news and entrepreneurship"""
        startup_data = self.raw_data.get('startups', {})
        
        all_startups = []
        all_startups.extend(startup_data.get('reddit_startups', []))
        all_startups.extend(startup_data.get('reddit_entrepreneur', []))
        
        top_startups = self.extract_top_items(all_startups, 'score', 5)
        
        return {
            'title': '🚀 Startups & Business',
            'items': top_startups,
            'summary': f"{len(top_startups)} insights from startup community"
        }
    
    def summarize_remote_jobs(self) -> Dict[str, Any]:
        """Summarize remote job opportunities and trends"""
        jobs_data = self.raw_data.get('remote_jobs', {})
        
        all_jobs = []
        all_jobs.extend(jobs_data.get('reddit_remotejobs', []))
        all_jobs.extend(jobs_data.get('reddit_forhire', []))
        
        top_jobs = self.extract_top_items(all_jobs, 'score', 6)
        
        return {
            'title': '💼 Remote Opportunities',
            'items': top_jobs,
            'summary': f"{len(top_jobs)} remote job posts and discussions"
        }
    
    def summarize_world_news(self) -> Dict[str, Any]:
        """Summarize important world news"""
        world_data = self.raw_data.get('world_news', {})
        
        all_news = []
        all_news.extend(world_data.get('reddit_worldnews', []))
        
        top_news = self.extract_top_items(all_news, 'score', 5)
        
        return {
            'title': '🌍 World News',
            'items': top_news,
            'summary': f"{len(top_news)} important global updates"
        }
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate complete intelligence summary"""
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
            'insights': self._generate_insights()
        }
        
        print("✅ Summary generated!")
        return summary
    
    def _generate_insights(self) -> List[str]:
        """Generate key insights from the data"""
        insights = [
            "📈 Focus areas today: Stay updated on AI developments and remote opportunities",
            "🎯 Action items: Check trending GitHub repos for learning opportunities",
            "💡 Remember: Knowledge compounds - what you learn today builds tomorrow's advantage"
        ]
        return insights
    
    def save_summary(self, summary: Dict[str, Any], output_path='data/summary.json'):
        """Save summary to file"""
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
    for section_name, section_data in summary['sections'].items():
        print(f"\n{section_data['title']}")
        print(f"  {section_data['summary']}")

if __name__ == "__main__":
    main()
