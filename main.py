#!/usr/bin/env python3
"""
Morning Intelligence Brief - Main Orchestrator
Runs the complete pipeline: scrape -> summarize -> email
"""

import sys
import os
from datetime import datetime

def main():
    print("="*60)
    print("☀️  MORNING INTELLIGENCE BRIEF")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S WIB')}")
    print("="*60)
    print()
    
    # Step 1: Scrape data
    print("Step 1/3: Scraping intelligence data...")
    print("-" * 60)
    from scraper import IntelligenceScraper
    scraper = IntelligenceScraper()
    data = scraper.collect_all_data()
    
    # Save raw data
    import json
    os.makedirs('data', exist_ok=True)
    with open('data/raw_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print()
    
    # Step 2: Generate summary
    print("Step 2/3: Generating intelligence summary...")
    print("-" * 60)
    from summarizer import IntelligenceSummarizer
    summarizer = IntelligenceSummarizer()
    summary = summarizer.generate_summary()
    summarizer.save_summary(summary)
    print()
    
    # Step 3: Send email
    print("Step 3/3: Sending email...")
    print("-" * 60)
    from email_sender import EmailGenerator
    
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    if not recipient_email:
        if len(sys.argv) > 1:
            recipient_email = sys.argv[1]
        else:
            print("❌ Error: No recipient email provided")
            print("Set RECIPIENT_EMAIL environment variable or pass as argument")
            sys.exit(1)
    
    generator = EmailGenerator()
    generator.send_email(to_email=recipient_email)
    print()
    
    print("="*60)
    print("✅ Morning Intelligence Brief completed successfully!")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S WIB')}")
    print("="*60)

if __name__ == "__main__":
    main()
