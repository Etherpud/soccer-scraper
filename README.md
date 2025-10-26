Soccer Scraper Microservice

This lightweight Flask app fetches and cleans public college athletics web pages (rosters, coaching staff, etc.) into plain text for AI enrichment pipelines.
It’s optimized for use with Zapier + OpenAI + Airtable flows and hosted free on Render
.

🚀 Overview

The service:

Accepts a ?url= query parameter.

Fetches the given web page with a browser-like User-Agent.

Strips out <script>, <style>, <img>, and other heavy tags.

Returns the readable text (trimmed to ~800 KB) as text/plain.

Example:

GET https://soccer-scraper.onrender.com/?url=https://goheels.com/sports/mens-soccer/coaches


Response → plain text containing all visible content from that page.

🧩 Files
File	Purpose
app.py	Flask application; fetches and cleans HTML.
requirements.txt	Python dependencies.
Procfile	Instructs Render to launch with Gunicorn.
⚙️ Local testing
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py


Visit http://localhost:10000/?url=https://goheels.com/sports/mens-soccer/coaches

☁️ Deploying to Render

Push to GitHub

git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOURNAME/soccer-scraper.git
git push -u origin main


Render Setup

Go to Render → New → Web Service

Connect your GitHub repo.

Choose:

Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app

Instance Type: Free

Click Deploy Web Service

Wait a few minutes for build & deploy.

Your live endpoint will look like:

https://soccer-scraper.onrender.com/?url=https://fightingirish.com/sports/mens-soccer/roster

🔗 Integration with Zapier

In your Webhooks → GET step, set:

https://soccer-scraper.onrender.com/?url={{Roster URL}}


or

https://soccer-scraper.onrender.com/?url={{Staff URL}}


Then map {{Get_Roster__RAW_BODY}} or {{Get_Coaches__RAW_BODY}} into your ChatGPT enrichment step.

🧰 Notes

Default timeout: 20 s

Text limit: ~800 KB

Handles redirects automatically.

Add extra HTML tags to strip by editing:

for tag in soup(["script", "style", "img", "svg", "noscript"]):
    tag.decompose()


Headers include a simple browser-style User-Agent to bypass most bot filters.

🩵 Example Output (truncated)
Men's Soccer Coaches
Head Coach: John Doe
Assistant Coach: Jane Smith
...

🧾 License

MIT — free to use and modify.
