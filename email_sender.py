#!/usr/bin/env python3
"""
Morning Intelligence Brief - Email Generator
Creates beautiful HTML emails from intelligence summaries
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from typing import Dict, Any, List

class EmailGenerator:
    def __init__(self, summary_path='data/summary.json'):
        with open(summary_path, 'r', encoding='utf-8') as f:
            self.summary = json.load(f)
    
    def generate_html_email(self) -> str:
        """Generate professional HTML email"""
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .header {{
            border-bottom: 3px solid #2563eb;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            color: #1e293b;
            font-size: 28px;
        }}
        .date {{
            color: #64748b;
            font-size: 14px;
            margin-top: 5px;
        }}
        .section {{
            margin-bottom: 35px;
        }}
        .section-title {{
            font-size: 20px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e2e8f0;
        }}
        .item {{
            background-color: #f8fafc;
            border-left: 4px solid #3b82f6;
            padding: 12px 15px;
            margin-bottom: 12px;
            border-radius: 4px;
        }}
        .item-title {{
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 5px;
        }}
        .item-title a {{
            color: #2563eb;
            text-decoration: none;
        }}
        .item-title a:hover {{
            text-decoration: underline;
        }}
        .item-meta {{
            font-size: 13px;
            color: #64748b;
        }}
        .insights {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-top: 30px;
        }}
        .insights h3 {{
            margin-top: 0;
            font-size: 18px;
        }}
        .insights ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .insights li {{
            margin-bottom: 8px;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
            text-align: center;
            color: #64748b;
            font-size: 13px;
        }}
        .repo {{
            background-color: #fff;
            border: 1px solid #e2e8f0;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 6px;
        }}
        .repo-name {{
            font-weight: 600;
            color: #2563eb;
            margin-bottom: 5px;
        }}
        .repo-desc {{
            font-size: 14px;
            color: #475569;
            margin-bottom: 5px;
        }}
        .repo-meta {{
            font-size: 12px;
            color: #64748b;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>☀️ Morning Intelligence Brief</h1>
            <div class="date">{self.summary['date']} • Generated at {self.summary['time_generated']}</div>
        </div>
        
        {self._generate_tech_section()}
        {self._generate_ai_ml_section()}
        {self._generate_startups_section()}
        {self._generate_remote_jobs_section()}
        {self._generate_world_news_section()}
        
        <div class="insights">
            <h3>💡 Key Insights for Today</h3>
            <ul>
                {self._generate_insights_list()}
            </ul>
        </div>
        
        <div class="footer">
            <p>Morning Intelligence Brief • Automated Daily Digest</p>
            <p>Stay informed, stay ahead 🚀</p>
        </div>
    </div>
</body>
</html>
        """
        return html
    
    def _generate_tech_section(self) -> str:
        tech = self.summary['sections']['tech_news']
        items_html = ""
        
        for item in tech['items'][:8]:
            items_html += f"""
            <div class="item">
                <div class="item-title">
                    <a href="{item.get('url', '#')}" target="_blank">{item.get('title', 'No title')}</a>
                </div>
                <div class="item-meta">
                    👍 {item.get('score', 0)} points • 💬 {item.get('comments', 0)} comments
                </div>
            </div>
            """
        
        return f"""
        <div class="section">
            <div class="section-title">{tech['title']}</div>
            {items_html}
        </div>
        """
    
    def _generate_ai_ml_section(self) -> str:
        ai_ml = self.summary['sections']['ai_ml']
        
        discussions_html = ""
        for item in ai_ml['discussions'][:6]:
            # Only show subreddit label if it exists and is not N/A
            subreddit_label = f" • r/{item['subreddit']}" if item.get('subreddit') and item.get('subreddit') != 'N/A' else ""
            discussions_html += f"""
            <div class="item">
                <div class="item-title">
                    <a href="{item.get('url', '#')}" target="_blank">{item.get('title', 'No title')}</a>
                </div>
                <div class="item-meta">
                    👍 {item.get('score', 0)} points • 💬 {item.get('comments', 0)} comments{subreddit_label}
                </div>
            </div>
            """
        
        repos_html = ""
        for repo in ai_ml.get('trending_repos', [])[:3]:
            repos_html += f"""
            <div class="repo">
                <div class="repo-name">
                    <a href="{repo.get('url', '#')}" target="_blank">⭐ {repo.get('name', 'Unknown')}</a>
                </div>
                <div class="repo-desc">{repo.get('description', 'No description')}</div>
                <div class="repo-meta">
                    ⭐ {repo.get('stars', 0)} stars • {repo.get('language', 'Unknown')}
                </div>
            </div>
            """
        
        return f"""
        <div class="section">
            <div class="section-title">{ai_ml['title']}</div>
            {discussions_html}
            {f'<h4 style="margin-top: 20px; color: #475569;">🔥 Trending Repositories</h4>{repos_html}' if repos_html else ''}
        </div>
        """
    
    def _generate_startups_section(self) -> str:
        startups = self.summary['sections']['startups']
        items_html = ""
        
        for item in startups['items'][:5]:
            items_html += f"""
            <div class="item">
                <div class="item-title">
                    <a href="{item.get('url', '#')}" target="_blank">{item.get('title', 'No title')}</a>
                </div>
                <div class="item-meta">
                    👍 {item.get('score', 0)} points • 💬 {item.get('comments', 0)} comments
                </div>
            </div>
            """
        
        return f"""
        <div class="section">
            <div class="section-title">{startups['title']}</div>
            {items_html}
        </div>
        """
    
    def _generate_remote_jobs_section(self) -> str:
        jobs = self.summary['sections']['remote_jobs']
        items_html = ""
        
        for item in jobs['items'][:6]:
            items_html += f"""
            <div class="item">
                <div class="item-title">
                    <a href="{item.get('url', '#')}" target="_blank">{item.get('title', 'No title')}</a>
                </div>
                <div class="item-meta">
                    👍 {item.get('score', 0)} points • 💬 {item.get('comments', 0)} comments
                </div>
            </div>
            """
        
        return f"""
        <div class="section">
            <div class="section-title">{jobs['title']}</div>
            {items_html}
        </div>
        """
    
    def _generate_world_news_section(self) -> str:
        news = self.summary['sections']['world_news']
        items_html = ""
        
        for item in news['items'][:5]:
            items_html += f"""
            <div class="item">
                <div class="item-title">
                    <a href="{item.get('url', '#')}" target="_blank">{item.get('title', 'No title')}</a>
                </div>
                <div class="item-meta">
                    👍 {item.get('score', 0)} points • 💬 {item.get('comments', 0)} comments
                </div>
            </div>
            """
        
        return f"""
        <div class="section">
            <div class="section-title">{news['title']}</div>
            {items_html}
        </div>
        """
    
    def _generate_insights_list(self) -> str:
        insights = self.summary.get('insights', [])
        return "\n".join([f"<li>{insight}</li>" for insight in insights])
    
    def send_email(self, 
                   to_email: str,
                   from_email: str = None,
                   smtp_password: str = None,
                   smtp_server: str = 'smtp.gmail.com',
                   smtp_port: int = 587):
        """Send the intelligence brief via email"""
        
        from_email = from_email or os.getenv('SMTP_EMAIL')
        smtp_password = smtp_password or os.getenv('SMTP_PASSWORD')
        
        if not from_email or not smtp_password:
            raise ValueError("Email credentials not provided")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"☀️ Morning Intelligence Brief - {self.summary['date']}"
        msg['From'] = from_email
        msg['To'] = to_email
        
        # Attach HTML
        html_part = MIMEText(self.generate_html_email(), 'html')
        msg.attach(html_part)
        
        # Send email
        try:
            print(f"📧 Sending email to {to_email}...")
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(from_email, smtp_password)
            server.send_message(msg)
            server.quit()
            print("✅ Email sent successfully!")
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            raise

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python email_sender.py <recipient_email>")
        sys.exit(1)
    
    recipient = sys.argv[1]
    
    generator = EmailGenerator()
    generator.send_email(to_email=recipient)

if __name__ == "__main__":
    main()
