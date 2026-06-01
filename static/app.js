const form = document.getElementById("searchForm");
const input = document.getElementById("userInput");
const resultsDiv = document.getElementById("results");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    console.log("BUTTON CLICKED");
    const text = input.value;
    const response = await fetch(
        "/recommend",
        { method: "POST",
            headers: {
            "Content-Type": "application/json"},
            body: JSON.stringify({
                text: text})}
    );
    const data = await response.json();
    displayResults(data);
});

function displayResults(data) {
    resultsDiv.innerHTML = "";
    resultsDiv.innerHTML += `
        <div class="section">
            <h2>Detected Topics</h2>
            <p>${data.detected_topics.join(", ")}</p>
        </div>
        <div class="section">
            <h2>Detected Styles</h2>
            <p>${data.detected_styles.join(", ")}</p>
        </div>
        <div class="section">
            <h2>Inferred Styles</h2>
            <p>${data.inferred_styles.join(", ")}</p>
        </div>
    `;

    resultsDiv.innerHTML += `
        <h2 class="recommend-title">
            Recommendations
        </h2>
    `;
    data.recommendations.forEach((rapper) => {
        resultsDiv.innerHTML += `
            <div class="rapper-card">
                <h3>${rapper.name}</h3>
                <p>
                    Final Score:
                    ${rapper.final_score.toFixed(2)}
                </p>
                <p>
                    Similarity:
                    ${rapper.similarity_score.toFixed(2)}
                </p>
            </div>
        `;});
}