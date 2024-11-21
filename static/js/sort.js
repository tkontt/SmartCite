document.querySelectorAll("table").forEach((table) => {
    table.querySelectorAll("th").forEach((header, columnIndex) => {
        if (header.getAttribute("id") == "actions") return;
        header.addEventListener("click", () => {
            // Toggle sort direction
            let currentDirection = header.getAttribute("data-sort") || "none";
            let newDirection = currentDirection === "asc" ? "desc" : "asc";
            header.setAttribute("data-sort", newDirection);

            // Remove sorting indicators from other headers
            table.querySelectorAll("th").forEach((h) => {
                if (h !== header) h.removeAttribute("data-sort");
            });

            // Sort rows based on the selected column
            sortTable(table, columnIndex, newDirection);

            // Update header text to show sorting indicator
            table.querySelectorAll("th").forEach((h) => {
                h.textContent = h.textContent.replace("▲", "").replace("▼", "").trim();
            });
            header.textContent += newDirection === "asc" ? " ▲" : " ▼";
        });
    });
});

function sortTable(table, columnIndex, newDirection) {
    let rows = Array.from(table.querySelectorAll("tbody tr"));

    rows.sort((rowA, rowB) => {
        let cellA = rowA.cells[columnIndex]?.textContent.trim() || "";
        let cellB = rowB.cells[columnIndex]?.textContent.trim() || "";

        if (newDirection === "asc") {
            if (cellA > cellB) {
                return 1;
            } else if (cellA < cellB) {
                return -1;
            } else {
                // If the values are equal, keep order unchanged
                return 0;
            }
        } else {
            if (cellA < cellB) {
                return 1;
            } else if (cellA > cellB) {
                return -1;
            } else {
                // If the values are equal, keep order unchanged
                return 0;
            }
        }
    });

    let tbody = table.querySelector("tbody");
    rows.forEach((row) => tbody.appendChild(row));
}
