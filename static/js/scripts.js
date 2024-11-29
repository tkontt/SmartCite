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

function copyToClipboard(text, message) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert(message || `Copied to clipboard: ${text}`);
    });
}

function showAlert(message, duration = 2000) {
    const alertContainer = document.getElementById('alert-container');
    
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show';
    alert.role = 'alert';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    alertContainer.appendChild(alert);

    setTimeout(() => {
        alert.classList.remove('show');
        alert.classList.add('fade');
        setTimeout(() => alert.remove(), 150);
    }, duration);
}