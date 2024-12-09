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
    unpublished: ["author", "title"],
    url: ["url"] // URL citation type only requires the URL field initially
};

// Ylläpitää listaa kentistä
let CURRENTFIELDS = [];
let mandatoryFields;
let optionalFields;
let getFields;
let addField;

function formFieldData(fields, citationType, citationId, citationKey) {
    const fieldData = JSON.parse(fields);
    CURRENTFIELDS = Object.keys(fieldData);
    console.log(CURRENTFIELDS, "Current fields");


    mandatoryFields = document.getElementById("mandatory-fields-edit");
    optionalFields = document.getElementById("optional-fields-edit");
    getFields = document.getElementById("get-fields-edit");
    addField = document.getElementById("add-field-edit");
    console.log(mandatoryFields, "mandatory fields");


    document.getElementById("edit-citation-card-header").innerHTML = `${citationKey} ${citationType} ${citationId}`;
    document.getElementById("citation_id-edit").value = citationId;
    document.getElementById("citation_type-edit").value = citationType;

    updateGetFields();
    clearAllFields();
    
    for (const fieldName in fieldData) {
        const isMandatory = MANDATORY[citationType]?.includes(fieldName);
        let placement = isMandatory ? mandatoryFields : optionalFields;
        
        createField(fieldName, fieldData[fieldName], placement, placement == optionalFields);
    }
}

function formForNewCitation(element) {
    mandatoryFields = document.getElementById("mandatory-fields-new");
    optionalFields = document.getElementById("optional-fields-new");
    getFields = document.getElementById("get-fields-new");
    addField = document.getElementById("add-field-new");

    updateFormAfterTypeChange(element);
}

function clearAllFields() {
    var last;
    while (last = mandatoryFields.lastChild) mandatoryFields.removeChild(last);
    while (last = optionalFields.lastChild) optionalFields.removeChild(last);
}

function updateGetFields() {
    getFields.value = `${CURRENTFIELDS}`;
}

function updateFormAfterTypeChange(element) {
    clearAllFields();

    const citationType = element.value;
    CURRENTFIELDS = MANDATORY[citationType].slice();
    updateGetFields();

    if (citationType === "url") {
        // URL-specific handling
        createField("url", "", mandatoryFields, false);
        
        // Add a button to fetch metadata
        const fetchButton = document.createElement("button");
        fetchButton.setAttribute("type", "button");
        fetchButton.setAttribute("class", "btn btn-secondary my-2");
        fetchButton.innerText = "Fetch Metadata";
        fetchButton.addEventListener("click", () => fetchUrlMetadata());
        mandatoryFields.appendChild(fetchButton);
    } else {
        // Normal handling for other citation types
        for (const fieldName of MANDATORY[citationType]) {
            createField(fieldName, "", mandatoryFields, false);
        }
    }
}

function fetchUrlMetadata() {
    const urlField = document.querySelector("input[name='url']");
    const url = urlField.value.trim();

    if (!url) {
        alert("Please enter a URL.");
        return;
    }

    fetch(`/fetch_metadata`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        // Dynamically populate fields with fetched metadata
        if (data.title) createField("title", data.title, optionalFields, true);
        if (data.author) createField("author", data.author, optionalFields, true);
        if (data.description) createField("description", data.description, optionalFields, true);
    })
    .catch(error => {
        console.error("Error fetching metadata:", error);
        alert("Failed to fetch metadata. Please try again.");
    });
}


function createRemoveButton(fieldName) {
    let removeButton = document.createElement("input");
    removeButton.setAttribute("type", "button");
    removeButton.setAttribute("value", "remove");

    removeButton.addEventListener("click", function () {
        removeButton.parentNode.remove();

        CURRENTFIELDS = CURRENTFIELDS.filter(value => value !== fieldName);
        updateGetFields();
    });

    return removeButton;
}

function createField(fieldName, fieldValue, placement, removable) {
    let container = document.createElement("div");
    container.setAttribute("class", "mb-3");

    let uniqueId = fieldName;

    let lbl = document.createElement("label");
    lbl.setAttribute("for", uniqueId);
    lbl.setAttribute("class", "form-label");
    lbl.innerText = `${fieldName}:`;

    let txt = document.createElement("input");
    txt.setAttribute("type", "text");
    txt.setAttribute("class", "form-control");
    txt.setAttribute("name", uniqueId);
    txt.setAttribute("id", uniqueId);
    txt.setAttribute("value", fieldValue || "");
    txt.required = true;

    container.appendChild(lbl);
    container.appendChild(txt);

    if (removable) {
        const removeButton = createRemoveButton(fieldName);
        container.appendChild(removeButton);
    }

    placement.appendChild(container);
}

function addNewField(loopIndex) {
    let placement = optionalFields;
    let nameOfNewField = addField.value.trim().toLowerCase();

    if (nameOfNewField === "") return;
    if (CURRENTFIELDS.includes(nameOfNewField)) return;

    CURRENTFIELDS.push(nameOfNewField);
    updateGetFields();
    createField(nameOfNewField, "", placement, true);
    addField.value = "";
}