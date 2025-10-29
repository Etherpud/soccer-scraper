import os
import re
import requests
from flask import Flask, request, jsonify, Response
from bs4 import BeautifulSoup

app = Flask(__name__)

# ---------------------------
# Healthcheck / keep-alive
# ---------------------------
@app.route("/health")
def health():
    return "ok", 200


def fetch_url(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    # remove heavy/irrelevant nodes
    for tag in soup(["script", "style", "img", "svg", "noscript", "source", "picture", "iframe"]):
        tag.decompose()
    # get readable text
    text = soup.get_text(separator="\n")
    # normalize whitespace and collapse excessive blank lines
    text = re.sub(r"\r", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = text.strip()
    # cap output (keeps Zapier happy)
    return text[:800_000]


# ---------------------------
# Main scraper endpoint
#   - GET  /scrape?url=...
#   - POST /scrape  { "url": "...", "format": "html|text" }
# Default format: text (stripped)
# ---------------------------
@app.route("/scrape", methods=["GET", "POST"])
def scrape():
    if request.method == "POST":
        body = request.get_json(silent=True) or {}
        url = body.get("url")
        fmt = (body.get("format") or "text").lower()
    else:
        url = request.args.get("url")
        fmt = (request.args.get("format") or "text").lower()

    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        html = fetch_url(url)
        if fmt == "html":
            return Response(html, mimetype="text/html; charset=utf-8"), 200
        # default: return cleaned text
        text = html_to_text(html)
        return Response(text, mimetype="text/plain; charset=utf-8"), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# Root route (handy for tests)
# ---------------------------
@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "endpoints": ["/scrape", "/health"],
        "usage": {
            "GET": "/scrape?url=https://example.com&format=text|html",
            "POST": {"url": "https://example.com", "format": "text|html"}
        }
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

