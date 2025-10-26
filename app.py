from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def fetch():
    url = request.args.get("url")
    if not url:
        return "Missing ?url=", 400

    try:
        r = requests.get(
            url,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0 (compatible; GPT-Scraper/1.0)"}
        )
        r.raise_for_status()
    except Exception as e:
        return f"Error fetching URL: {e}", 500

    # Strip scripts, styles, images
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "img", "svg", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator="\n")

    # Limit size (Render free tier limit ≈ 50 MB, but keep it lean)
    text = text[:800000]
    return Response(text, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
