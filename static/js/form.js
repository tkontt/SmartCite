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

const OPTIONAL = {
    article: ["volume", "number", "pages", "month", "note"],
    book: ["volume", "number", "pages", "month", "note"],
    inproceedings: ["booktitle ", "year", "editor", "volume", "number", "series", "pages", "month",
                    "address", "organization", "publisher", "note", "annote"],
    booklet: ["author", "howpublished", "address", "month", "year", "note", "annote"],
    conference: ["booktitle ", "year", "editor", "volume", "number", "series", "pages", "month", "address",
                 "organization", "publisher", "note", "annote"],
    inbook: ["volume", "number", "series", "type", "address", "edition", "pages", "month", "note", "annote"],
    incollection: ["publisher", "year", "editor", "volume", "number", "series", "type", "chapter", "address",
                   "edition", "pages", "month", "note", "annote"],
    manual: ["author", "organization", "address", "edition", "month", "year", "note", "annote"],
    masterthesis: ["type", "address", "month", "note", "annote"],
    misc: [],
    phdthesis: ["type", "address", "month", "note", "annote"],
    proceedings: ["booktitle ", "editor", "volume", "number", "series", "month", "address", "organization", 
                  "publisher", "note", "annote"],
    techreport: ["type", "number", "address", "month", "note", "annote"],
    unpublished: ["month", "year", "note", "annote"],
};

// Ylläpitää listaa kentistä
let CURRENTFIELDS = [];
let MODAL;

let mandatoryFields;
let optionalFields;
let addField;
let addFieldErrorCont;
let getFields;

function formFieldData(fields, citationType, citationId, citationKey) {
    const fieldData = JSON.parse(fields);
    CURRENTFIELDS = Object.keys(fieldData);
    MODAL = "edit";

    updateModal();

    document.getElementById("edit-citation-card-header").innerHTML = `${citationKey} ${citationType}`;
    document.getElementById("citation_id-edit").value = citationId;
    document.getElementById("citation_type-edit").value = citationType;

    updateGetFields();
    clearAllFields();
    
    for (const fieldName in fieldData) {
        const isMandatory = MANDATORY[citationType]?.includes(fieldName);
        let placement = isMandatory ? mandatoryFields : optionalFields;
        
        createField(fieldName, fieldData[fieldName], placement, placement == optionalFields);
    }
    populateDatalist(citationType);
    addField.value = "";
}

function formForNewCitation(element) {
    MODAL = "new";
    updateModal();
    updateFormAfterTypeChange(element);
}

function updateModal() {
    mandatoryFields = document.getElementById(`mandatory-fields-${MODAL}`);
    optionalFields = document.getElementById(`optional-fields-${MODAL}`);
    getFields = document.getElementById(`get-fields-${MODAL}`);
    addField = document.getElementById(`add-field-${MODAL}`);
    addFieldErrorCont = document.getElementById(`add-field-error-${MODAL}`);
}

function clearAllFields() {
    var last;
    while (last = mandatoryFields.lastChild) mandatoryFields.removeChild(last);
    while (last = optionalFields.lastChild) optionalFields.removeChild(last);
    while (last = addFieldErrorCont.lastChild) addFieldErrorCont.removeChild(last);
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
        populateDatalist(citationType);
        addField.value = "";
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
    let removeButton = document.createElement("button");
    removeButton.setAttribute("type", "button");
    removeButton.setAttribute("class", "btn btn-danger btn-sm ms-2");
    removeButton.setAttribute("value", "remove");
    removeButton.innerText = "Remove";

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

    let lbl = document.createElement("label");
    lbl.setAttribute("for", fieldName);
    lbl.setAttribute("class", "form-label");
    lbl.innerText = `${fieldName}:`;

    let txt = document.createElement("input");
    txt.setAttribute("type", "text");
    txt.setAttribute("class", "form-control");
    txt.setAttribute("name", fieldName);
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

function addNewField() {
    let placement = optionalFields;
    let nameOfNewField = addField.value.trim().toLowerCase();

    let message = null;
    if (nameOfNewField == "") message = "Please name the field.";
    if (CURRENTFIELDS.includes(nameOfNewField)) message = "A field with the given name already exists.";
    if (message) {
        showAlert(message, 2000, `add-field-error-${MODAL}`, 'alert-danger');
        return;
    }

    CURRENTFIELDS.push(nameOfNewField);
    updateGetFields();
    createField(nameOfNewField, "", placement, true);
    addField.value = "";
}

function populateDatalist(citationType) {
    const datalist = document.getElementById(`add-field-dl-${MODAL}`);

    var last;
    while (last = datalist.lastChild) datalist.removeChild(last);

    for (const fieldName of OPTIONAL[citationType]) {
        const option = document.createElement("option");
        option.innerText = fieldName;
        datalist.appendChild(option);
    }
}