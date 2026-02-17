# ☀️ Morning Intelligence Brief

Automated daily email digest that provides you with summaries about:
- 💻 Tech News & Development
- 🤖 AI & Machine Learning Updates
- 🚀 Startup & Business Insights
- 💼 Remote Job Opportunities
- 🌍 World News

**100% Free** • **Fully Automated** • **Professional Email Format**

---

## 🎯 Features

- ✅ Scrapes data from HackerNews, Reddit, GitHub Trending
- ✅ AI-powered summarization & ranking
- ✅ Beautiful HTML email format
- ✅ Runs automatically every morning at 7 AM WIB
- ✅ Zero cost (free tier everything)
- ✅ GitHub Actions automation

---

## 🚀 Quick Setup (15 minutes)

### Step 1: Fork Repository

1. Click the **Fork** button on GitHub
2. Clone your repo to local (optional, for testing)

### Step 2: Setup Email (Gmail)

You need 2 Gmail accounts:
- **Account A**: Email that will **RECEIVE** the brief (your daily email)
- **Account B**: Email that will **SEND** the brief (create a new one, it's free)

#### Setup Account B (Sender Email):

1. Create a new Gmail (example: `myintelligencebrief@gmail.com`)
2. Enable **2-Step Verification**:
   - Go to: https://myaccount.google.com/security
   - Enable "2-Step Verification"
3. Generate **App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Other" → type "Morning Brief"
   - Click **Generate**
   - **COPY** the password (16 characters, e.g.: `abcd efgh ijkl mnop`)

### Step 3: Setup GitHub Secrets

In your GitHub repo, go to:
**Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add 3 secrets:

| Name | Value | Example |
|------|-------|---------|
| `RECIPIENT_EMAIL` | Your email that receives the brief | `yourname@gmail.com` |
| `SMTP_EMAIL` | Email sender (Account B) | `myintelligencebrief@gmail.com` |
| `SMTP_PASSWORD` | App password from Account B | `abcd efgh ijkl mnop` |

**Optional** (if you want to use NewsAPI - free tier):
| Name | Value | How to get |
|------|-------|------------|
| `NEWS_API_KEY` | API key | Register at https://newsapi.org/register (free) |

### Step 4: Activate GitHub Actions

1. Go to the **Actions** tab in your repo
2. Click **"I understand my workflows, go ahead and enable them"**
3. Done! The workflow will run automatically at 7 AM WIB

---

## 🧪 Manual Testing

To test immediately without waiting for 7 AM:

### Option 1: GitHub Actions (Recommended)

1. Go to the **Actions** tab
2. Click **"Morning Intelligence Brief"** workflow
3. Click the **"Run workflow"** dropdown
4. Click the **"Run workflow"** button
5. Wait ~30-60 seconds
6. Check your email!

### Option 2: Local Testing

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/morning-intelligence-brief.git
cd morning-intelligence-brief

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export RECIPIENT_EMAIL="your@email.com"
export SMTP_EMAIL="sender@gmail.com"
export SMTP_PASSWORD="your-app-password"

# Run
python main.py
```

---

## 📧 Email Preview

Your email will look like this:

```
☀️ Morning Intelligence Brief
Friday, February 14, 2026 • Generated at 07:00 WIB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💻 Tech & Development

📌 New Python 3.13 Release: Performance Improvements
   👍 1,234 points • 💬 567 comments

📌 GitHub Copilot Workspace: AI-powered Development
   👍 987 points • 💬 234 comments

[... more items ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 AI & Machine Learning

📌 GPT-5 Rumors: What We Know So Far
   👍 2,345 points • 💬 890 comments

🔥 Trending Repositories

⭐ username/awesome-llm-apps
   A curated list of LLM applications
   ⭐ 12,345 stars • Python

[... more sections ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Key Insights for Today

📈 Focus areas today: Stay updated on AI developments
🎯 Action items: Check trending repos for learning
💡 Remember: Knowledge compounds
```

---

## ⚙️ Customization

### Change Schedule

Edit `.github/workflows/morning-brief.yml`:

```yaml
schedule:
  - cron: '0 0 * * *'  # 00:00 UTC = 07:00 WIB
```

For other times (WIB = UTC + 7):
- 06:00 WIB → `cron: '0 23 * * *'`
- 08:00 WIB → `cron: '0 1 * * *'`
- 09:00 WIB → `cron: '0 2 * * *'`

### Add Data Sources

Edit `scraper.py`, add subreddit or other sources:

```python
def collect_all_data(self):
    data = {
        # ... existing sources ...
        'new_category': {
            'reddit_mysubreddit': self.fetch_reddit_hot('mysubreddit', 5),
        }
    }
```

### Change Email Template

Edit `email_sender.py` in the `generate_html_email()` section to customize style/layout.

---

## 🐛 Troubleshooting

### Email not arriving?

1. **Check spam folder**
2. **Verify secrets** in GitHub (Settings → Secrets)
3. **Check Actions logs**: Actions tab → click workflow run → view error
4. **Gmail app password** correct? Must be 16 characters without spaces
5. **2-Step Verification** enabled in Gmail?

### Workflow not running?

1. **Check Actions enabled**: Actions tab → enable workflows
2. **Manual trigger**: Actions → Run workflow
3. **Check logs**: Click workflow run → see which step failed

### Empty data?

- HackerNews/Reddit might be rate limiting
- Wait a few minutes, try again
- Check internet connection in GitHub Actions

---

## 📊 Data Sources

- **HackerNews**: Top stories (tech, startup, programming)
- **Reddit**: r/programming, r/technology, r/MachineLearning, r/LocalLLaMA, r/startups, r/remotejs, r/forhire, r/worldnews
- **GitHub Trending**: Python repos (AI/ML focus)
- **NewsAPI** (optional): Global tech & business news

---

## 💰 Cost Breakdown

- ✅ GitHub Actions: **FREE** (2,000 minutes/month)
- ✅ Gmail SMTP: **FREE**
- ✅ HackerNews API: **FREE**
- ✅ Reddit API: **FREE** (no auth needed for public data)
- ✅ GitHub API: **FREE** (60 requests/hour)
- ✅ NewsAPI: **FREE** (100 requests/day)

**Total: $0/month** 🎉

---

## 🔒 Privacy & Security

- ✅ No data collection
- ✅ No third-party services (except email)
- ✅ Secrets encrypted by GitHub
- ✅ Open source (audit it yourself)
- ✅ Runs on GitHub infrastructure (trusted)

---

## 🎓 For Students

Do you have **GitHub Student Developer Pack**? Great! Although this system is already free, you get bonuses:
- GitHub Actions: Unlimited minutes (vs 2,000)
- Private repos: Unlimited
- And many other tools for development

---

## 🚀 What's Next?

- [ ] Add market data (stocks, crypto)
- [ ] Add weather forecast
- [ ] Mobile app version
- [ ] Slack/Discord/Telegram integration
- [ ] Personalized filtering (AI-based)
- [ ] Weekly summary reports

---

## 🤝 Contributing

You can improve this system:
1. Fork the repo
2. Make changes
3. Submit a pull request

Ideas welcome! 💡

---

## 📝 License

MIT License - use it, modify it, share it as you like.

---

## 💬 Support

Having issues? 
1. Check the troubleshooting section
2. Check GitHub Actions logs
3. Open a GitHub issue

---

**Built with ❤️ for students who hustle**

Stay informed. Stay ahead. 🚀
