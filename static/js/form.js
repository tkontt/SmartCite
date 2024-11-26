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
      article: ["author", "title", "journal", "year"],
      book: ["author", "editor", "title", "publisher", "year"],
      inproceedings: ["author", "title"],
      booklet: ["title"],
      conference: ["author", "title"],
      inbook: ["author", "title", "chapter", "publisher", "year"],
      incollection: ["author", "title", "booktitle"],
      manual: ["title"],
      masterthesis: ["author", "title", "school", "year"],
      misc: [],
      phdthesis: ["author", "title", "school", "year"],
      proceedings: ["title", "year"],
      techreport: ["author", "title", "institution", "year"],
      unpublished: ["author", "title"]
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
        txt.setAttribute("type", "text");
        txt.setAttribute("class", "form-control");
        txt.setAttribute("name", field);
        txt.required = true;
      
        f.appendChild(lbl);
        f.appendChild(txt);
        placement.appendChild(f);
    }

    for (field of types[type]) {
      createField(field);
    }
}