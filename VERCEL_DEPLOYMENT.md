# 🚀 Vercel Deployment & Update Guide
## AI Career Companion Platform

Since Hostinger is currently unavailable, the deployment pipeline has been updated to use **Vercel** as the primary web hosting platform.

---

## 🔄 The New Pipeline Architecture

```mermaid
flowchart LR
    A["1. Local Files / File Manager"] -->|"git commit & push"| B["2. GitHub Repo (main)"]
    B -->|"Auto-Deploy Webhook"| C["3. Vercel (Serverless Python)"]
    B -.->|"Optional Backup"| D["Render Service"]
    C -->|"Direct HTTPS Live URL"| E["*.vercel.app or Custom Domain"]
```

1. **File Manager / IDE**: You edit files in your local workspace.
2. **GitHub**: You commit and push to `origin main`.
3. **Vercel**: Vercel listens to GitHub pushes, triggers an automated serverless build via `api/index.py` and `vercel.json`, and serves your app globally via high-speed edge CDN.
4. **Custom Domain**: Optionally attach `ai-career-companion.pnpstudio.in` or any domain directly in Vercel with free auto-renewing SSL.

---

## 🛠️ One-Time Setup on Vercel (Takes 2 Minutes)

### Step 1: Log in to Vercel
1. Go to [vercel.com](https://vercel.com) and sign in with your **GitHub account**.

### Step 2: Import the GitHub Repository
1. Click the **"Add New..."** button (top right) → select **"Project"**.
2. Find your repository: **`pnpstudio2008/CareerPath-AI`** (or search for `CareerPath-AI`).
3. Click **"Import"**.

### Step 3: Configure Project Settings
- **Framework Preset**: Leave as **Other** (Vercel automatically detects `vercel.json` and Python runtime).
- **Root Directory**: `./` (leave default).
- **Build Command**: Leave default.
- **Output Directory**: Leave default.

### Step 4: Add Environment Variables
In the **Environment Variables** section on Vercel, add the following key-value pairs (matching your Supabase Cloud PostgreSQL database):

| Variable Key | Value | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql://postgres.vggpjzbhumvlkckkxhxv:Parth%409586368646@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres?sslmode=require` | Supabase Cloud Pooler Connection |
| `SECRET_KEY` | `itmsls-career-companion-secure-key-2025` | Flask Session Security Key |
| `PG_HOST` | `aws-0-ap-northeast-1.pooler.supabase.com` | PostgreSQL Host |
| `PG_PORT` | `5432` | PostgreSQL Port |
| `PG_DATABASE` | `postgres` | Database Name |
| `PG_USER` | `postgres.vggpjzbhumvlkckkxhxv` | Database User |
| `PG_PASSWORD` | `Parth@9586368646` | Database Password |

### Step 5: Click "Deploy"
- Click **"Deploy"**. Vercel will install dependencies from `requirements.txt`, bundle `templates/` and `static/`, and deploy your app in 30–60 seconds!
- You will receive a live URL: `https://careerpath-ai.vercel.app` (or similar).

---

## 🌐 Connecting Your Custom Domain (`pnpstudio.in`)

When you are ready to point your domain/subdomain to Vercel:
1. In your Vercel Dashboard, go to your project → **Settings** → **Domains**.
2. Add your subdomain: e.g. `ai-career-companion.pnpstudio.in` (or `companion.pnpstudio.in`).
3. Vercel will show a **CNAME** DNS record:
   - **Type**: `CNAME`
   - **Name / Host**: `ai-career-companion`
   - **Value / Target**: `cname.vercel-dns.com`
4. Add this CNAME record in your domain DNS manager (Cloudflare, GoDaddy, Namecheap, etc.).
5. Vercel automatically generates and provisions a free **Let's Encrypt SSL Certificate**.

---

## 🔁 Everyday Update Workflow (How to push updates)

Whenever you make changes to files:

1. **Edit files in File Manager / VS Code**.
2. **Commit and push to GitHub**:
   ```bash
   git add .
   git commit -m "Describe your changes"
   git push origin main
   ```
3. **That's it!** Vercel automatically detects the push and deploys the new version within 20 seconds.
   - No need to log into Hostinger hPanel.
   - No need to zip files or upload via web file managers.
   - Zero downtime deployment with instant rollback capabilities.

---

## 📁 Key Project Files for Vercel

- `vercel.json` — Vercel routing rules, memory allocation, and inclusion of HTML templates and static files.
- `api/index.py` — Python WSGI entrypoint that loads your Flask `app`.
- `.vercelignore` — Prevents temporary, cache, and test files from being uploaded.
- `requirements.txt` — Python dependencies installed automatically during build.
