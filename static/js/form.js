document.addEventListener("DOMContentLoaded", function() {
    updateForm(document.getElementById("citation_type"))
});

function updateForm(element) {
    var placement = document.getElementById("mandatory_fields");

    // Tyhjennä edelliset kentät
    var last;
    while (last = placement.lastChild) placement.removeChild(last);

    // Pakolliset kentät
    let types = {
      book: ["author", "editor", "title", "publisher", "year"],
      article: ["author", "title", "journal", "year"],
      inproceedings: ["author", "title"]
    }

    const type = element.value;

    // Luo pakolliset kentät valitulle tyypille
    function createField(field) {
        var f = document.createElement("div");
        f.setAttribute("class", "mb-3");
            
        var lbl = document.createElement("label");
        lbl.setAttribute("for", field);
        lbl.setAttribute("class", "form-label");
        lbl.innerHTML = `${field}:`;
      
        var txt = document.createElement("input");
        lbl.setAttribute("type", "text");
        lbl.setAttribute("class", "form-control");
        lbl.setAttribute("name", field);
      
        f.appendChild(lbl);
        f.appendChild(txt);
        placement.appendChild(f);
    }

    createField("key");

    for (field of types[type]) {
      createField(field);
    }
}