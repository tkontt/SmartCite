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
