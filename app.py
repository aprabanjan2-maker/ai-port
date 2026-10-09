from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    url = data.get("url", "").strip()

    if not url:
        return jsonify({
            "success": False,
            "error": "Portfolio URL is required."
        }), 400

    # Add HTTPS if the user didn't type it
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "AIPort Portfolio Analyzer/1.0"
            }
        )

        response.raise_for_status()

    except requests.RequestException as e:

        return jsonify({
            "success": False,
            "error": "Unable to access this portfolio website."
        }), 400


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    # -------------------------
    # BASIC WEBSITE ANALYSIS
    # -------------------------

    title = soup.title

    title_text = (
        title.get_text(strip=True)
        if title
        else ""
    )


    description = soup.find(
        "meta",
        attrs={"name": "description"}
    )


    viewport = soup.find(
        "meta",
        attrs={"name": "viewport"}
    )


    headings = soup.find_all(
        ["h1", "h2", "h3"]
    )


    images = soup.find_all("img")


    images_without_alt = [
        img for img in images
        if not img.get("alt")
    ]


    links = soup.find_all("a")


    https_score = 10 if url.startswith(
        "https://"
    ) else 0


    title_score = 15 if title_text else 0


    description_score = (
        10 if description else 0
    )


    viewport_score = (
        10 if viewport else 0
    )


    heading_score = (
        10 if len(headings) > 0 else 0
    )


    image_score = 15

    if len(images) > 0:

        if len(images_without_alt) == 0:
            image_score = 15

        else:
            image_score = 8


    # -------------------------
    # CATEGORY SCORES
    # -------------------------

    seo_score = min(
        100,
        title_score +
        description_score +
        https_score +
        heading_score
    )


    accessibility_score = 100

    if len(images) > 0:

        missing_percentage = (
            len(images_without_alt)
            / len(images)
        )

        accessibility_score = round(
            100 -
            (missing_percentage * 50)
        )


    responsive_score = (
        100 if viewport else 50
    )


    content_score = min(
        100,
        50 +
        (10 if title_text else 0) +
        (10 if len(headings) > 0 else 0) +
        (10 if len(links) > 2 else 0)
    )


    performance_score = 85


    ui_score = round(
        (
            responsive_score +
            accessibility_score +
            content_score
        ) / 3
    )


    overall_score = round(
        (
            ui_score +
            responsive_score +
            seo_score +
            accessibility_score +
            content_score +
            performance_score
        ) / 6
    )


    # -------------------------
    # SUGGESTIONS
    # -------------------------

    suggestions = []


    if not title_text:

        suggestions.append(
            "Add a clear and descriptive page title."
        )


    if not description:

        suggestions.append(
            "Add a meta description for better SEO."
        )


    if not viewport:

        suggestions.append(
            "Add a responsive viewport meta tag."
        )


    if images_without_alt:

        suggestions.append(
            f"Add alt text to "
            f"{len(images_without_alt)} image(s)."
        )


    if not headings:

        suggestions.append(
            "Add proper heading structure using H1, H2 and H3."
        )


    if not suggestions:

        suggestions.append(
            "Your basic website structure looks good. "
            "Continue improving performance and UX."
        )


    return jsonify({

        "success": True,

        "url": url,

        "scores": {

            "ui": ui_score,

            "responsive": responsive_score,

            "seo": seo_score,

            "accessibility": accessibility_score,

            "content": content_score,

            "performance": performance_score,

            "overall": overall_score
        },

        "suggestions": suggestions,

        "website": {

            "title": title_text,

            "images": len(images),

            "links": len(links),

            "headings": len(headings)

        }

    })


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
