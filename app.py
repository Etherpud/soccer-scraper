import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ----------------------------------------------------
# Simple health check (for Render / uptime monitors)
# ----------------------------------------------------
@app.route("/health")
def health():
    return "ok", 200


# ----------------------------------------------------
# Main scraper endpoint (supports GET + POST)
# ----------------------------------------------------
@app.route("/scrape", methods=["GET", "POST"])
def scrape():
    # Accept URL either from query string or JSON body
    if request.method == "POST":
        body = request.get_json(silent=True) or {}
        url = body.get("url")
    else:
        url = request.args.get("url")

    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        # Fetch the remote page
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # Return plain text (Zapier handles HTML/text fine)
        return response.text, 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# ----------------------------------------------------
# Default route (for quick browser tests)
# ----------------------------------------------------
@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "endpoints": ["/scrape", "/health"],
        "usage": "POST or GET /scrape?url=https://example.com"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

