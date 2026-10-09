function toggleMenu() {

    const menu = document.getElementById("menu");

    menu.classList.toggle("show");

}


function analyzePortfolio() {

    const url =
        document.getElementById("portfolioURL").value.trim();

    const message =
        document.getElementById("message");


    if (url === "") {

        message.textContent =
            "Please enter your portfolio URL.";

        return;

    }


    try {

        new URL(url);

    } catch {

        message.textContent =
            "Please enter a valid URL.";

        return;

    }


    message.textContent =
        "Analyzing portfolio...";


    document.getElementById("reviewURL").textContent =
        url;


    /*
       DEMO SCORES

       Later we will replace these
       with REAL AI analysis.
    */

    setTimeout(() => {

        const scores = {

            ui: 88,
            responsive: 92,
            seo: 76,
            accessibility: 84,
            content: 90,
            performance: 81

        };


        const overall = Math.round(

            (
                scores.ui +
                scores.responsive +
                scores.seo +
                scores.accessibility +
                scores.content +
                scores.performance

            ) / 6

        );


        document.getElementById("overallScore")
            .textContent = overall;

        document.getElementById("uiScore")
            .textContent = scores.ui;

        document.getElementById("responsiveScore")
            .textContent = scores.responsive;

        document.getElementById("seoScore")
            .textContent = scores.seo;

        document.getElementById("accessibilityScore")
            .textContent = scores.accessibility;

        document.getElementById("contentScore")
            .textContent = scores.content;

        document.getElementById("performanceScore")
            .textContent = scores.performance;


        const suggestions =
            document.getElementById("suggestionList");


        suggestions.innerHTML = `

            <div class="suggestion">
                🔍 Improve your SEO title and meta description.
            </div>

            <div class="suggestion">
                📱 Test your navigation on smaller mobile screens.
            </div>

            <div class="suggestion">
                ⚡ Optimize large images to improve loading speed.
            </div>

            <div class="suggestion">
                ♿ Add better accessibility labels to interactive elements.
            </div>

        `;


        message.textContent =
            "Portfolio analysis completed!";


        document.getElementById("results")
            .scrollIntoView({
                behavior: "smooth"
            });


    }, 1500);

}