# ☀️ Morning Intelligence Brief

Automated daily email digest yang kasih lo ringkasan tentang:
- 💻 Tech News & Development
- 🤖 AI & Machine Learning Updates
- 🚀 Startup & Business Insights
- 💼 Remote Job Opportunities
- 🌍 World News

**100% Free** • **Fully Automated** • **Professional Email Format**

---

## 🎯 Features

- ✅ Scrapes data dari HackerNews, Reddit, GitHub Trending
- ✅ AI-powered summarization & ranking
- ✅ Beautiful HTML email format
- ✅ Runs automatically setiap pagi jam 7 WIB
- ✅ Zero cost (free tier everything)
- ✅ GitHub Actions automation

---

## 🚀 Quick Setup (15 menit)

### Step 1: Fork Repository

1. Klik tombol **Fork** di GitHub
2. Clone repo lo ke local (optional, buat testing)

### Step 2: Setup Email (Gmail)

Lo butuh 2 Gmail accounts:
- **Account A**: Email yang bakal **NERIMA** brief (email lo sehari-hari)
- **Account B**: Email yang bakal **NGIRIM** brief (bikin baru aja, gratis)

#### Setup Account B (Sender Email):

1. Buat Gmail baru (contoh: `myintelligencebrief@gmail.com`)
2. Enable **2-Step Verification**:
   - Go to: https://myaccount.google.com/security
   - Enable "2-Step Verification"
3. Generate **App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Other" → tulis "Morning Brief"
   - Click **Generate**
   - **COPY** password (16 karakter, misal: `abcd efgh ijkl mnop`)

### Step 3: Setup GitHub Secrets

Di GitHub repo lo, go to:
**Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Tambahin 3 secrets:

| Name | Value | Example |
|------|-------|---------|
| `RECIPIENT_EMAIL` | Email lo yang nerima brief | `yourname@gmail.com` |
| `SMTP_EMAIL` | Email sender (Account B) | `myintelligencebrief@gmail.com` |
| `SMTP_PASSWORD` | App password dari Account B | `abcd efgh ijkl mnop` |

**Optional** (kalo mau pake NewsAPI - free tier):
| Name | Value | How to get |
|------|-------|------------|
| `NEWS_API_KEY` | API key | Daftar di https://newsapi.org/register (free) |

### Step 4: Activate GitHub Actions

1. Go to **Actions** tab di repo lo
2. Klik **"I understand my workflows, go ahead and enable them"**
3. Done! Workflow bakal jalan otomatis jam 7 pagi WIB

---

## 🧪 Testing Manual

Buat test langsung tanpa nunggu jam 7 pagi:

### Option 1: GitHub Actions (Recommended)

1. Go to **Actions** tab
2. Klik **"Morning Intelligence Brief"** workflow
3. Klik **"Run workflow"** dropdown
4. Klik **"Run workflow"** button
5. Wait ~30-60 detik
6. Check email lo!

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

Email lo bakal keliatan kayak gini:

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

### Ubah Jadwal

Edit `.github/workflows/morning-brief.yml`:

```yaml
schedule:
  - cron: '0 0 * * *'  # 00:00 UTC = 07:00 WIB
```

Untuk jam lain (WIB = UTC + 7):
- 06:00 WIB → `cron: '0 23 * * *'`
- 08:00 WIB → `cron: '0 1 * * *'`
- 09:00 WIB → `cron: '0 2 * * *'`

### Tambah Source Data

Edit `scraper.py`, tambahin subreddit atau source lain:

```python
def collect_all_data(self):
    data = {
        # ... existing sources ...
        'new_category': {
            'reddit_mysubreddit': self.fetch_reddit_hot('mysubreddit', 5),
        }
    }
```

### Ubah Email Template

Edit `email_sender.py` di bagian `generate_html_email()` buat customize style/layout.

---

## 🐛 Troubleshooting

### Email ga sampai?

1. **Check spam folder**
2. **Verify secrets** di GitHub (Settings → Secrets)
3. **Check Actions logs**: Actions tab → klik workflow run → lihat error
4. **Gmail app password** bener? Harus 16 karakter tanpa spasi
5. **2-Step Verification** udah enable di Gmail?

### Workflow ga jalan?

1. **Check Actions enabled**: Actions tab → enable workflows
2. **Manual trigger**: Actions → Run workflow
3. **Check logs**: Klik workflow run → lihat step mana yang fail

### Data kosong?

- HackerNews/Reddit mungkin rate limiting
- Tunggu beberapa menit, coba lagi
- Check internet connection di GitHub Actions

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
- ✅ Open source (audit sendiri)
- ✅ Runs on GitHub infra (trusted)

---

## 🎓 For Students

Lo punya **GitHub Student Developer Pack**? Mantap! Meskipun system ini udah gratis, lo dapet bonus:
- GitHub Actions: Unlimited minutes (vs 2,000)
- Private repos: Unlimited
- Dan banyak tools lain buat development

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

Lo bisa improve system ini:
1. Fork repo
2. Bikin changes
3. Submit pull request

Ideas welcome! 💡

---

## 📝 License

MIT License - pake sesuka lo, modify sesuka lo, share sesuka lo.

---

## 💬 Support

Ada masalah? 
1. Check troubleshooting section
2. Check GitHub Actions logs
3. Open GitHub issue

---

**Built with ❤️ for students who hustle**

Stay informed. Stay ahead. 🚀
