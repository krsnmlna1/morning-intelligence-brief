# 🔧 Troubleshooting Guide

## Email Tidak Sampai

### 1. Check Spam/Junk Folder
- Gmail kadang mark automated emails sebagai spam
- Check folder "Promotions" atau "Updates" juga
- Kalo ketemu, mark as "Not Spam"

### 2. Verify GitHub Secrets
```
Settings → Secrets and variables → Actions

Pastikan ada 3 secrets:
✅ RECIPIENT_EMAIL
✅ SMTP_EMAIL  
✅ SMTP_PASSWORD
```

### 3. Check Gmail App Password
- App password harus 16 karakter (format: `abcd efgh ijkl mnop`)
- BUKAN password Gmail biasa
- Harus dari https://myaccount.google.com/apppasswords
- 2-Step Verification harus enabled dulu

### 4. Check GitHub Actions Logs
```
Actions tab → Klik workflow run → Lihat error

Common errors:
❌ "Authentication failed" → App password salah
❌ "Connection refused" → SMTP server issue (coba lagi)
❌ "Recipient address rejected" → Email typo
```

### 5. Test Manual di Local
```bash
# Clone repo
git clone <your-repo-url>
cd morning-intelligence-brief

# Setup .env
cp .env.example .env
# Edit .env dengan credentials lo

# Run test
chmod +x test-local.sh
./test-local.sh
```

---

## Workflow Tidak Jalan

### 1. Actions Belum Enabled
```
Actions tab → "I understand my workflows, go ahead and enable them"
```

### 2. Manual Trigger
```
Actions → "Morning Intelligence Brief" → "Run workflow"
```

### 3. Schedule Belum Aktif
- Workflow pertama kali harus di-trigger manual
- Setelah itu baru schedule aktif otomatis

### 4. Repo Private tapi bukan Pro/Student
- Free GitHub account: 2,000 minutes/month
- Cek usage: Settings → Billing → Actions

---

## Data Kosong atau Sedikit

### Rate Limiting
- Reddit/HackerNews/GitHub punya rate limits
- Tunggu beberapa menit, coba lagi
- Ga akan affect daily automation (kecuali spam run manual)

### Network Issues di GitHub Actions
- Jarang terjadi, biasanya temporary
- Workflow otomatis retry besok pagi

### Subreddit Private/Banned
- Kalo subreddit private, ga bisa di-scrape
- Edit `scraper.py` ganti dengan subreddit lain

---

## Error: "Module not found"

```bash
# Install dependencies
pip install -r requirements.txt

# Atau di GitHub Actions, check step "Install dependencies" success
```

---

## Error: "Permission denied"

```bash
# Local testing
chmod +x test-local.sh
chmod +x main.py
```

---

## Email Format Rusak

### Gambar tidak muncul
- Email HTML ga support external images by default
- Ini normal, design udah dioptimasi tanpa gambar

### Style tidak konsisten
- Beberapa email client (Outlook) render HTML berbeda
- Gmail/Yahoo/ProtonMail tested OK
- Kalo pake Outlook, mungkin style slightly different

---

## Timezone Salah

### Email datang jam yang salah
Edit `.github/workflows/morning-brief.yml`:

```yaml
# WIB = UTC + 7
# Jadi buat jam 7 WIB (pagi), set UTC jam 0 (midnight)

schedule:
  - cron: '0 0 * * *'  # 07:00 WIB

# Contoh lain:
# 06:00 WIB → '0 23 * * *'
# 08:00 WIB → '0 1 * * *'  
# 09:00 WIB → '0 2 * * *'
```

---

## Performance Issues

### Email terlalu panjang
Edit di `summarizer.py`:

```python
# Kurangi limit items
top_tech = self.extract_top_items(all_tech, 'score', 5)  # was 8
```

### Workflow timeout
- Free tier: max 6 hours per job (lebih dari cukup)
- Typical run: 30-60 detik
- Kalo timeout, ada issue di network/API

---

## FAQ

**Q: Bisa pake email selain Gmail?**
A: Bisa, tapi harus support SMTP. Edit `email_sender.py`:
```python
smtp_server='smtp.outlook.com'  # Outlook
smtp_server='smtp.mail.yahoo.com'  # Yahoo
```

**Q: Bisa kirim ke multiple emails?**
A: Bisa! Set `RECIPIENT_EMAIL` dengan comma-separated:
```
RECIPIENT_EMAIL=email1@gmail.com,email2@gmail.com
```
Then edit `email_sender.py` untuk split & loop.

**Q: Bisa custom hari (weekday only)?**
A: Edit workflow cron:
```yaml
# Senin-Jumat only
- cron: '0 0 * * 1-5'
```

**Q: Data dari Indonesia/bahasa Indonesia?**
A: Tambahin subreddit Indonesia di `scraper.py`:
```python
'reddit_indonesia': self.fetch_reddit_hot('indonesia', 5)
```

**Q: Bisa tambahin crypto/stock prices?**
A: Bisa! Pake free APIs:
- CoinGecko API (crypto)
- Alpha Vantage (stocks - free tier)
Edit `scraper.py` tambahin method baru.

---

## Still Having Issues?

1. **Re-read README.md** - especially setup steps
2. **Check all secrets** - typo is common mistake
3. **Try manual trigger first** before expecting daily automation
4. **Check Actions logs** - error message usually clear
5. **Open GitHub Issue** - with error logs & description

---

**99% masalah karena:**
- ❌ App password salah (bukan password Gmail biasa!)
- ❌ 2-Step Verification belum enabled
- ❌ Typo di email address
- ❌ Secrets belum di-set atau salah nama

**Fix ini dulu sebelum panic!** 😅
