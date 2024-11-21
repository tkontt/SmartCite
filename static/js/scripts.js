// static/js/scripts.js
//Rivin tuplaklikkaus
document.addEventListener("DOMContentLoaded", function() {
    const rows = document.querySelectorAll(".citation-row");

    rows.forEach(function(row) {
        row.addEventListener("dblclick", function() {
            // Hae citation ID rivin data-id attribuutilta
            const citationId = row.getAttribute("data-id");
            
            // ohjaa edit sivulle
            window.location.href = `/citation/${citationId}`;
        });
    });
});

// Hakutoiminno Javascript
function filterTable() {
    const input = document.getElementById("search-input");
    const filter = input.value.toLowerCase();
    const table = document.getElementById("citations-table");
    const rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) { // Aloita riviltä 1, skippaa header row
        const cells = rows[i].getElementsByTagName("td");
        let rowText = "";
        for (let j = 0; j < cells.length; j++) {
            rowText += cells[j].textContent.toLowerCase();
        }
        rows[i].style.display = rowText.includes(filter) ? "" : "none";
    }
}

// Kopioi latex key clipboardille
function copyToClipboard(text) {
        const tempInput = document.createElement("textarea");
        tempInput.value = text;
        document.body.appendChild(tempInput);
        tempInput.select();
        try {
            document.execCommand("copy");
            alert("Copied to clipboard: " + text);
        } catch (err) {
            alert("Failed to copy text. Please try again.");
        }
        document.body.removeChild(tempInput);
}
