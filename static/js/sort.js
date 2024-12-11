document.querySelectorAll("table").forEach((table) => {
    // Store the original order of rows
    let originalRows = Array.from(table.querySelectorAll("tbody tr"));

    table.querySelectorAll("th").forEach((header, columnIndex) => {
        if (header.getAttribute("id") == "actions") return;
        header.addEventListener("click", () => {
            // Toggle sort direction
            let currentDirection = header.getAttribute("data-sort") || "none";
            let newDirection;
            if (currentDirection === "none") {
                newDirection = "asc";
            } else if (currentDirection === "asc") {
                newDirection = "desc";
            } else {
                newDirection = "none";
            }
            header.setAttribute("data-sort", newDirection);

            // Remove sorting indicators from other headers
            table.querySelectorAll("th").forEach((h) => {
                if (h !== header) h.removeAttribute("data-sort");
            });

            // Sort rows based on the selected column or reset to original order
            if (newDirection === "none") {
                resetTable(table, originalRows);
            } else {
                sortTable(table, columnIndex, newDirection);
            }

            // Update header text to show sorting indicator
            table.querySelectorAll("th").forEach((h) => {
                h.textContent = h.textContent.replace("▲", "").replace("▼", "").trim();
            });
            if (newDirection !== "none") {
                header.textContent += newDirection === "asc" ? " ▲" : " ▼";
            }
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

function resetTable(table, originalRows) {
    let tbody = table.querySelector("tbody");
    originalRows.forEach((row) => tbody.appendChild(row));
}
