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

let CURRENTFIELDS = [];

function updateAllFieldsElementValue() {
    const element = document.getElementById("all-fields");
    element.value = `${CURRENTFIELDS}`;
}

function formFieldData(fields, citationType, citationId) {
    const fieldData = JSON.parse(fields);
    CURRENTFIELDS = Object.keys(fieldData);
    updateAllFieldsElementValue();
    const mandatoryFields = document.getElementById("mandatory-fields");
    const optionalFields = document.getElementById("optional-fields");
    
    for (const fieldName in fieldData) {
        const mandatory = MANDATORY[citationType].includes(fieldName);
        let placement = mandatory ? mandatoryFields : optionalFields;
        
        createField(fieldName, fieldData[fieldName], placement, placement == optionalFields);

        if (!mandatory) {
            const removeButton = document.getElementById(`remove-${fieldName}`);
            removeButton.addEventListener("click", function() {
                fetch(`/remove_citation_field/${citationId}/${fieldName}`, {method: 'POST'})
                .then(response => response.json()) 
                .then(data => console.log(data)) 
                .catch(error => console.error(error));
            })
        }
    }
}

function createField(fieldName, fieldValue, placement, removable) {
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
    txt.setAttribute("value", fieldValue);
    txt.required = true;

    container.appendChild(lbl);
    container.appendChild(txt);
    if (removable) container.appendChild(createRemoveButton(fieldName));
    placement.appendChild(container);
}

function createRemoveButton(fieldName) {
    let removeButton = document.createElement("input");
    removeButton.setAttribute("type", "button");
    removeButton.setAttribute("value", "Remove");
    removeButton.setAttribute("id", `remove-${fieldName}`);

    removeButton.addEventListener("click", function() {
        let fieldContainer = document.getElementById(`${fieldName}-container`);
        document.getElementById("optional-fields").removeChild(fieldContainer);

        CURRENTFIELDS = CURRENTFIELDS.filter(function(value) {
          return value != fieldName;
        });
        updateAllFieldsElementValue();
    });

    return removeButton;
}

function addNewField() {
    let placement = document.getElementById("optional-fields");
    let nameOfNewField = document.getElementById("add-field").value.trim().toLowerCase();

    if (nameOfNewField == "") return;
    if (CURRENTFIELDS.includes(nameOfNewField)) return; // Virheviesti syötteestä kesken

    CURRENTFIELDS.push(nameOfNewField);
    updateAllFieldsElementValue();
    createField(nameOfNewField, "", placement, true);
    document.getElementById("add-field").value = "";
}
