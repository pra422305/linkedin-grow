# LinkGrow AI

LinkGrow AI is a final-year Computer Engineering project: an intelligent LinkedIn growth assistant for profile analysis, post drafting, networking recommendations, engagement analytics, and weekly growth planning.

It stores the user's LinkedIn profile URL so recommendations and drafts are tied to the correct profile. It does not directly track private profile views from the URL alone; profile views and post analytics must be entered manually or imported from an authorized source. It does not guarantee likes, impressions, followers, or connections. It does not scrape LinkedIn or automate likes, comments, follows, messages, or connection requests.

## Setup on Windows

```powershell
cd "C:\Users\LENOVO\Documents\New project\LinkGrowAI"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
flask --app app.py init-db
flask --app app.py run
```

Open http://127.0.0.1:5000.

## Database

SQLite is the default local option. For MySQL, set `DATABASE_URL` in `.env`:

```text
DATABASE_URL=mysql+pymysql://user:password@localhost/linkgrow_ai
```

## LinkedIn Metrics Sync

Users can save their LinkedIn profile URL during registration. This helps the app personalize recommendations and identify which profile the analytics belong to.

Direct fetching of impressions, likes, comments, and profile views requires an authorized LinkedIn API integration. A public profile link alone cannot provide private analytics and the app does not scrape LinkedIn.

For a real authorized integration, configure:

```text
LINKEDIN_ACCESS_TOKEN=your_authorized_oauth_token
LINKEDIN_API_VERSION=202610
```

The Analytics page includes a `Sync LinkedIn Metrics` button. Without an authorized token, it shows a setup message and keeps the manual analytics form available.

## Dataset Pipeline

The dataset was inspected on Hugging Face on 2026-10-14. The repository shows Apache-2.0 license, `posts.csv`, and 258 train rows.

```powershell
python -m ml.preprocess "https://huggingface.co/datasets/NeuML/neuml-linkedin-202501/resolve/main/posts.csv"
```

If internet access is unavailable, download an authorized CSV manually and run:

```powershell
python -m ml.preprocess data/raw/posts.csv
```

## Training

```powershell
python -m ml.train_classifier
python -m ml.train_engagement_model
```

The classifier uses weak, reviewable labels when human labels are unavailable. The engagement model uses verified engagement-rate data only when enough rows exist.

## Tests

```powershell
pytest
```

## Troubleshooting

- If Flask cannot import modules, confirm you are inside the `LinkGrowAI` folder.
- If MySQL fails, use SQLite first, then verify the MySQL server, database, username, password, and `PyMySQL` install.
- If dataset download fails, use the local CSV import path.
- If LLM keys are absent, the app uses deterministic template-based generation.
