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
// 
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

//JS  - Checkboksit taulukon headereille

// "Refe "Select all" boxille"
const selectAllCheckbox = document.getElementById('select-all');
const headerCheckboxes = document.querySelectorAll('.header-checkbox');

// Handlaa "Select All" checkbox muutokset
selectAllCheckbox.addEventListener('change', function() {
    const isChecked = this.checked;
    // Vaihda checkboksit/taulut
    headerCheckboxes.forEach(checkbox => {
        checkbox.checked = isChecked;
        const columnIndex = checkbox.dataset.column;
        const table = document.getElementById('citations-table');
        
        table.querySelectorAll('tr').forEach(row => {
            const cell = row.children[columnIndex];
            if (cell) {
                cell.style.display = isChecked ? '' : 'none';
            }
        });
    });
});

// Handlaa yksittäisten boksien chekkaukset suhteessa "Select all" boksiin
headerCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        // Jos mikä tahansa boksi unchekataan -> unchekkaa "Select all"
        if (!this.checked) {
            selectAllCheckbox.checked = false;
        }
        // Jos kaikki boksit chekattuna, chekkaa "Select all" 
        else if ([...headerCheckboxes].every(cb => cb.checked)) {
            selectAllCheckbox.checked = true;
        }

        const columnIndex = this.dataset.column;
        const table = document.getElementById('citations-table');
        
        table.querySelectorAll('tr').forEach(row => {
            const cell = row.children[columnIndex];
            if (cell) {
                cell.style.display = this.checked ? '' : 'none';
            }
        });
    });
});

