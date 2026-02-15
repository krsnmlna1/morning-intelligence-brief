# 📁 Project Structure

```
morning-intelligence-brief/
├── .github/
│   └── workflows/
│       └── morning-brief.yml      # GitHub Actions automation (runs at 7 AM WIB)
│
├── data/                          # Created at runtime (gitignored)
│   ├── raw_data.json             # Scraped data from all sources
│   └── summary.json              # Processed & summarized data
│
├── scraper.py                     # Main scraper - fetches from multiple sources
├── summarizer.py                  # AI summarizer - processes raw data
├── email_sender.py                # Email generator - creates & sends HTML email
├── main.py                        # Orchestrator - runs complete pipeline
│
├── requirements.txt               # Python dependencies (minimal!)
├── .env.example                   # Template for environment variables
├── .gitignore                     # Git ignore rules
│
├── test-local.sh                  # Local testing script (bash)
│
├── README.md                      # Complete documentation
├── QUICKSTART.md                  # 15-minute setup guide
├── TROUBLESHOOTING.md             # Common issues & solutions
├── PROJECT_STRUCTURE.md           # This file
└── email-preview.html             # Visual preview of email output
```

---

## 📄 File Descriptions

### Core Scripts

**scraper.py**
- Fetches data from HackerNews, Reddit, GitHub
- No authentication required (all public APIs)
- Returns structured JSON data
- ~200 lines, well-commented

**summarizer.py**
- Processes raw data into digestible summaries
- Ranks items by score/popularity
- Extracts top items per category
- Generates key insights
- ~150 lines

**email_sender.py**
- Generates professional HTML email
- Beautiful responsive design
- Sends via Gmail SMTP
- ~300 lines (mostly HTML template)

**main.py**
- Orchestrates complete workflow
- Scrape → Summarize → Email
- Simple, clean pipeline
- ~50 lines

---

## ⚙️ Configuration Files

**.github/workflows/morning-brief.yml**
- GitHub Actions workflow
- Scheduled to run at 00:00 UTC (07:00 WIB)
- Installs dependencies
- Runs main.py
- Uses GitHub Secrets for credentials

**.env.example**
- Template for local development
- Copy to `.env` and fill in your credentials
- Not committed to git

**requirements.txt**
- Only 1 dependency: `requests`
- Intentionally minimal
- Python standard library for everything else

---

## 📊 Data Flow

```
1. GitHub Actions (scheduled 7 AM WIB)
   ↓
2. main.py (orchestrator)
   ↓
3. scraper.py
   ├── HackerNews API
   ├── Reddit JSON endpoints
   ├── GitHub API
   └── (Optional) NewsAPI
   ↓
4. data/raw_data.json (saved)
   ↓
5. summarizer.py
   ├── Rank by score
   ├── Extract top items
   ├── Generate insights
   └── Save to data/summary.json
   ↓
6. email_sender.py
   ├── Load summary.json
   ├── Generate HTML email
   ├── Connect to Gmail SMTP
   └── Send email
   ↓
7. Email arrives in your inbox! ☀️
```

---

## 🔐 Secrets (GitHub Actions)

Required in: `Settings → Secrets and variables → Actions`

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `RECIPIENT_EMAIL` | Your email (receives brief) | `you@gmail.com` |
| `SMTP_EMAIL` | Sender email (Gmail account) | `briefsender@gmail.com` |
| `SMTP_PASSWORD` | Gmail App Password (16 chars) | `abcd efgh ijkl mnop` |
| `NEWS_API_KEY` | Optional: NewsAPI key | `abc123def456...` |

---

## 🎨 Email Template

The email uses:
- **Inline CSS** (email clients don't support `<style>` tags well)
- **Gradient headers** for visual appeal
- **Responsive design** (works on mobile)
- **No external images** (faster loading)
- **Professional typography** (system fonts)

Color scheme:
- Primary: `#2563eb` (blue)
- Accent: `#667eea` → `#764ba2` (gradient)
- Background: `#f8fafc` (light gray)
- Text: `#1e293b` (dark gray)

---

## 🧪 Testing

### Local Testing
```bash
./test-local.sh
```

### Manual GitHub Actions
```
Actions → Morning Intelligence Brief → Run workflow
```

### Check Logs
```
Actions → [workflow run] → [job] → [step]
```

---

## 🔧 Customization Points

### Change Sources
Edit `scraper.py`:
```python
'your_category': {
    'reddit_yoursubreddit': self.fetch_reddit_hot('yoursubreddit', 5),
}
```

### Change Email Layout
Edit `email_sender.py` → `generate_html_email()` method

### Change Schedule
Edit `.github/workflows/morning-brief.yml`:
```yaml
cron: '0 0 * * *'  # 07:00 WIB
```

### Change Number of Items
Edit `summarizer.py`:
```python
top_tech = self.extract_top_items(all_tech, 'score', 8)  # Change 8 to desired number
```

---

## 💾 Data Storage

**Raw Data** (`data/raw_data.json`):
- All scraped data before processing
- Kept for debugging/auditing
- Uploaded as GitHub Actions artifact (7 days retention)

**Summary** (`data/summary.json`):
- Processed, ranked data
- Ready for email template
- Also uploaded as artifact

Both files are **gitignored** (not committed to repo).

---

## 🚀 Deployment

**Zero setup needed!**
- Runs on GitHub infrastructure
- No server required
- No hosting costs
- No maintenance

Just:
1. Set secrets
2. Enable Actions
3. Done!

---

## 📈 Future Enhancements

Possible additions (community contributions welcome):

- [ ] Market data (stocks, crypto)
- [ ] Weather forecast
- [ ] Calendar integration
- [ ] AI-powered personalization
- [ ] Multiple email recipients
- [ ] Slack/Discord webhooks
- [ ] Mobile app
- [ ] Weekly summary report
- [ ] Read later integration (Pocket, Instapaper)

---

## 🤝 Contributing

Want to improve this project?

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Test locally with `./test-local.sh`
5. Submit pull request

See `CONTRIBUTING.md` for guidelines (TBD).

---

## 📝 License

MIT License - Free to use, modify, and distribute.

---

**Questions?** Check README.md or TROUBLESHOOTING.md first!
