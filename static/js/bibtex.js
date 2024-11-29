document.getElementById("bibtex_button").addEventListener("click", function () {
    fetchBibTeX();
});
const bibtexList = document.getElementById("bibtex-list");

function fetchBibTeX() {
    fetch('/create_bibtex')
    .then(response => {
        return response.text();
    })
    .then(data => {
        bibtexList.textContent = data;
    })
}

function copyBibTex() {
    const bibtexContent = bibtexList.textContent;
    copyToClipboard(bibtexContent, "BibTeX copied to clipboard");
}

function downloadBibTex() {
    const bibtexContent = bibtexList.textContent;
    const blob = new Blob([bibtexContent]);
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "citations.bib";
    link.click();
}