# 🚀 Hostinger Deployment Guide
## AI Career Companion → `ai-career-companion.pnpstudio.in`

---

## Step 1 — Create the Subdomain in hPanel

1. Log in to **hPanel** → **Domains** → **Subdomains**
2. Click **Create Subdomain**
3. Enter: `ai-career-companion` under `pnpstudio.in`
4. Hostinger will auto-create the folder:
   `/home/u<id>/domains/ai-career-companion.pnpstudio.in/public_html/`

---

## Step 2 — Upload Project Files via File Manager

1. Go to **hPanel** → **Files** → **File Manager**
2. Navigate to `/home/u<id>/domains/ai-career-companion.pnpstudio.in/public_html/`
3. Upload all project files (zip the project folder and extract here), OR use **Git** below.

### Option A — Upload via Git (Recommended)

SSH into Hostinger (Business/Cloud plans include SSH access):
```bash
ssh u<userid>@<your-server-ip>
cd /home/u<userid>/domains/ai-career-companion.pnpstudio.in/public_html/
git clone https://github.com/pnpstudio2008/CareerPath-AI.git .
```

### Option B — Upload via File Manager

1. Zip the entire project on your PC (excluding `__pycache__/`, `uploads/`, `.env`)
2. Upload the zip via File Manager
3. Extract in-place

---

## Step 3 — Create the `.env` File on Hostinger

**In File Manager**, inside `public_html/`, create a new file named `.env`:
```
DATABASE_URL=postgresql://postgres.vggpjzbhumvlkckkxhxv:Parth%409586368646@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres?sslmode=require
PG_HOST=aws-0-ap-northeast-1.pooler.supabase.com
PG_PORT=5432
PG_DATABASE=postgres
PG_USER=postgres.vggpjzbhumvlkckkxhxv
PG_PASSWORD=Parth@9586368646
SECRET_KEY=itmsls-career-companion-secure-key-2025
```
> ⚠️ **Never commit this file to GitHub.** It is listed in `.gitignore`.

---

## Step 4 — Set Up Python App in hPanel

1. Go to **hPanel** → **Advanced** → **Python App Manager**  
   *(or search "Python" in hPanel)*
2. Click **Create Application**
3. Fill in:
   | Field | Value |
   |---|---|
   | Python Version | `3.11` (highest available) |
   | Application Root | `domains/ai-career-companion.pnpstudio.in/public_html` |
   | Application URL | `ai-career-companion.pnpstudio.in` |
   | Application startup file | `passenger_wsgi.py` |
   | Application Entry Point | `application` |
4. Click **Create**

---

## Step 5 — Install Python Dependencies

In **Python App Manager**, after creating the app:
1. Click the **Enter to the virtual environment** button (or use the pip install section)
2. Install packages:
   ```bash
   pip install flask>=3.0.0 gunicorn>=21.2.0 psycopg2-binary>=2.9.9 python-dotenv>=1.0.0 pypdf>=5.0.0 requests>=2.31.0
   ```
   OR click **Run pip install** and enter the contents of `requirements.txt`

---

## Step 6 — Restart the Application

Click **Restart** in the Python App Manager. Your app should now be live at:
**https://ai-career-companion.pnpstudio.in**

---

## Step 7 — Enable HTTPS (SSL)

1. Go to **hPanel** → **SSL** → **SSL/TLS**
2. Enable **Free SSL (Let's Encrypt)** for `ai-career-companion.pnpstudio.in`
3. Enable **Force HTTPS** redirect

---

## Folder Structure on Hostinger

```
public_html/
├── passenger_wsgi.py    ← Hostinger entry point (DO NOT rename)
├── wsgi.py              ← Flask WSGI wrapper
├── app.py               ← Main Flask application
├── database.py          ← Supabase PostgreSQL layer
├── nlp_engine.py        ← AI/NLP resume analysis
├── mock_test_engine.py  ← Quiz/mock test engine
├── mailer.py            ← Email 2FA mailer
├── hiring_dataset.py    ← 45-company dataset loader
├── sample_resumes.py    ← Sample resume data
├── requirements.txt     ← Python dependencies
├── .env                 ← Environment secrets (create manually, NOT uploaded to Git)
├── .env.example         ← Template (safe to commit)
├── .gitignore
├── static/
│   ├── css/style.css
│   ├── js/
│   └── images/
├── templates/           ← HTML templates
├── data/                ← Synthetic datasets
├── uploads/             ← Temp uploaded resumes (auto-created)
└── ai_resume_models.pkl ← ML model file
```

---

## Updating the Site

When you push changes to GitHub, SSH in and run:
```bash
cd /home/u<userid>/domains/ai-career-companion.pnpstudio.in/public_html/
git pull origin main
```
Then click **Restart** in hPanel Python App Manager.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError` | Re-run `pip install -r requirements.txt` in the virtual env |
| `500 Internal Server Error` | Check logs: hPanel → Python App Manager → Error Logs |
| Database connection error | Verify `.env` values and Supabase pooler URL |
| Static files not loading | Ensure `static/` folder is present and Flask serves them |
| App shows old version | Click **Restart** in Python App Manager after `git pull` |
