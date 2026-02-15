# 🚀 Setup Cepat (15 Menit)

## Step-by-step buat lo yang buru-buru

### 1️⃣ Fork & Clone

```bash
# Klik "Fork" di GitHub, terus:
git clone https://github.com/USERNAME_LO/morning-intelligence-brief.git
cd morning-intelligence-brief
```

### 2️⃣ Bikin Gmail Baru (Sender)

1. Bikin Gmail baru: https://accounts.google.com/signup
   - Misal: `mymorningbrief@gmail.com`
   
2. Enable 2-Step Verification:
   - https://myaccount.google.com/security
   - Klik "2-Step Verification" → ikutin step-nya
   
3. Bikin App Password:
   - https://myaccount.google.com/apppasswords
   - App: Mail, Device: Other (tulis "Brief")
   - COPY password-nya (16 karakter)

### 3️⃣ Setup GitHub Secrets

Buka repo lo di GitHub:
**Settings → Secrets and variables → Actions → New repository secret**

Tambahin ini (satu-satu):

```
Name: RECIPIENT_EMAIL
Value: email-lo-yang-mau-nerima@gmail.com

Name: SMTP_EMAIL  
Value: mymorningbrief@gmail.com

Name: SMTP_PASSWORD
Value: abcd efgh ijkl mnop  (app password dari step 2)
```

### 4️⃣ Enable GitHub Actions

1. Klik tab **Actions**
2. Klik **"I understand my workflows, go ahead and enable them"**

### 5️⃣ Test Sekarang!

1. Tetep di tab **Actions**
2. Klik **"Morning Intelligence Brief"**
3. Klik **"Run workflow"** (dropdown)
4. Klik **"Run workflow"** (button hijau)
5. Tunggu ~1 menit
6. **Check email lo!** ☀️

---

## ✅ Selesai!

Mulai besok, lo bakal dapet email setiap jam **7 pagi WIB**.

**Email ga masuk?**
- Check spam folder
- Pastiin secrets udah bener semua
- Klik workflow run → lihat error log

**Mau ganti jam?**
- Edit `.github/workflows/morning-brief.yml`
- Ubah `cron: '0 0 * * *'` 
- 06:00 WIB = `'0 23 * * *'`
- 08:00 WIB = `'0 1 * * *'`

---

**Need help?** Baca README.md lengkap atau open issue di GitHub.

**Selamat job hunting! 🚀**
