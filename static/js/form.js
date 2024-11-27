document.addEventListener("DOMContentLoaded", function() {
    updateForm(document.getElementById("citation_type"))
});

// Pakolliset kentät
const MANDATORY = {
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
};

// Ylläpitää listaa kentistä
let current_fields = [];

function createField(fieldName, placement, removable) {
    let container = document.createElement("div");
    container.setAttribute("class", "mb-3");
    container.setAttribute("id", `${fieldName}-container`);
      
    let lbl = document.createElement("label");
    lbl.setAttribute("for", fieldName);
    lbl.setAttribute("class", "form-label");
    lbl.innerHTML = `${fieldName}:`;

    let txt = document.createElement("input");
    txt.setAttribute("type", "text");
    txt.setAttribute("class", "form-control");
    txt.setAttribute("name", fieldName);
    txt.required = true;

    container.appendChild(lbl);
    container.appendChild(txt);

    // Painike, jolla voi poistaa luodun/valinnaisen kentän
    if (removable) {
      let removeBtn = document.createElement("input");
      removeBtn.setAttribute("type", "button");
      removeBtn.setAttribute("value", "Remove");

      removeBtn.addEventListener("click", function() {
          let remove = document.getElementById(`${fieldName}-container`);
          document.getElementById("optional_fields").removeChild(remove);

          current_fields = current_fields.filter(function(value) {
              return value != fieldName;
          });
          setAllFields();
      });
      container.appendChild(removeBtn);
  };
  placement.appendChild(container);
}

function updateForm(element) {
    let placement = document.getElementById("mandatory_fields");
    let optionals = document.getElementById("optional_fields");

    // Tyhjennä edellisen valitun tyypin kentät
    var last;
    while (last = placement.lastChild) placement.removeChild(last);
    while (last = optionals.lastChild) optionals.removeChild(last);

    const type = element.value;
    current_fields = MANDATORY[type].slice();
    setAllFields();

    for (fieldName of MANDATORY[type]) createField(fieldName, placement, false);
}

function addNewField() {
    let placement = document.getElementById("optional_fields");
    let nameOfNewField = document.getElementById("add_field").value.trim().toLowerCase();

    if (nameOfNewField == "") return;
    if (current_fields.includes(nameOfNewField)) return; // Virheviesti syötteestä kesken

    current_fields.push(nameOfNewField);
    setAllFields();
    createField(nameOfNewField, placement, true);
    document.getElementById("add_field").value = "";
}

// Kentät asetetaan all_fields elementin valueksi
function setAllFields() {
    let element = document.getElementById("all_fields");
    element.value = `${current_fields}`;
}