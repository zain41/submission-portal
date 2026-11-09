from flask import Flask, request, render_template, redirect, url_for
from urllib.parse import urlparse

app = Flask(__name__)

# In-memory storage for submissions
submissions = []

def is_valid_url(url: str) -> bool:
    """Check if the URL has a valid http/https scheme and a domain."""
    try:
        result = urlparse(url)
        return result.scheme in ("http", "https") and bool(result.netloc)
    except Exception:
        return False

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        # Get data from the form and strip whitespace
        name = (request.form.get("name") or "").strip()
        reg_no = (request.form.get("reg_no") or "").strip()
        title = (request.form.get("title") or "").strip()
        url = (request.form.get("url") or "").strip()

        # Validation logic
        if not all([name, reg_no, title, url]):
            error = "All fields are required."
        elif not is_valid_url(url):
            error = "Invalid submission URL. Use a full http/https link."
        else:
            # Save the valid submission
            submissions.append({"name": name, "reg_no": reg_no, "title": title, "url": url})
            return redirect(url_for("index"))

    return render_template("index.html", submissions=submissions, error=error)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)