from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.citation_repository import (
    get_citations,
    add_citation,
)
from repositories.citation_repository import (
    delete_citation_from_db,
    update_citation_in_db,
    get_unique_field_names,
)
from entities.citation import Citation
from config import app, test_env
from util import (
    generate_cite_key,
    validate_fields,
    generate_bibtex,
    import_bibtex_citations,
    validate_bibtex,
)

TYPES = ["article", "book", "inproceedings", "booklet", "conference", "inbook", "incollection",
         "manual", "masterthesis", "misc", "phdthesis", "proceedings", "techreport", "unpublished"]


@app.route("/")
def index():
    types = list(filter(lambda x: x != "article", TYPES))
    all_fields = get_unique_field_names()
    default_headers = ["author", "title", "year", "type"]
    citations = get_citations()

    return render_template(
        "index.html",
        citations=citations,
        types=types,
        default_headers=default_headers,
        all_fields=all_fields,
    )


@app.route("/create_citation", methods=["POST"])
def citation_creation():
    citation_type = request.form.get("citation-type")
    fields = {}
    all_fields = request.form.get("get-fields-new").split(",")

    if all_fields == [""]:
        flash("Citation must at least have one field.")
        return redirect("/")

    for field in all_fields:
        fields[field] = request.form.get(field).strip()

    try:
        validate_fields(fields)
        key = generate_cite_key(fields)
        add_citation(Citation(citation_type, key, fields))
        flash("Citation added successfully!")
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/")


# Poista Citation
@app.route("/delete_citation/<int:citation_id>", methods=["POST"])
def delete_citation_route(citation_id):
    try:
        delete_citation_from_db(citation_id)
        flash("Citation deleted successfully!", "success")
    except Exception as e:
        flash(f"An error occurred while deleting: {e}", "danger")
    return redirect("/")


# Muokkaa
@app.route("/update_citation", methods=["POST"])
def edit_citation_form_route():
    citation_id = request.form.get("citation_id")
    all_fields = request.form.get("get-fields-edit").split(",")
    fields = {}

    if all_fields == [""]:
        delete_citation_from_db(citation_id)
        flash("Citation removed due to all fields being removed.")
        return redirect("/")

    for field in all_fields:
        fields[field] = request.form.get(field).strip()

    if "" in fields.values():
        flash("Citation edit failed due to some empty fields.")
        return redirect("/")

    citekey = update_citation_in_db(citation_id, fields)
    flash(f'Citation {citekey} edited successfully.')
    return redirect("/")


@app.route("/create_bibtex", methods=["GET"])
def create_bibtex():
    citations = get_citations()
    return generate_bibtex(citations)


@app.route("/import_citations_bibtex", methods=["POST"])
def import_from_bibtex(bibtex_input=None):
    if bibtex_input is None:
        bibtex = request.form.get("input_bibtex")
    else:
        bibtex = bibtex_input
    try:
        validate_bibtex(bibtex)
    except Exception as error:
        flash(str(error))
        return redirect("/")

    citations = import_bibtex_citations(bibtex)

    for c in citations:
        add_citation(c)
    if len(citations) == 1:
        flash(f"{len(citations)} citation added successfully!")
    else:
        flash(f"{len(citations)} citations added successfully!")
    return redirect("/")



@app.route('/upload', methods=['POST'])
def upload_bibtex_file():
    if 'file' not in request.files:
        flash("No file given")

    file = request.files['file']
    if file.filename == '':
        flash("No selected file")
    elif file:
        content = file.read()
        content = content.decode('utf-8')
        import_from_bibtex(content)
    return redirect("/")




# testausta varten oleva reitti

if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})

    @app.route("/create_test_citations")
    def create_test_citations():
        for i in range(1, 10):
            add_citation(
                Citation(
                    "article",
                    generate_cite_key(
                        {
                            "author": f"Author{i}",
                            "title": f"Title{i}",
                            "year": f"201{i}",
                            "journal": f"Journal{i}",
                        }
                    ),
                    {
                        "author": f"Author{i}",
                        "title": f"Title{i}",
                        "year": f"201{i}",
                        "journal": f"Journal{i}",
                        "custom_field": f"CustomField{i}",
                    },
                )
            )

        return jsonify({"message": "created test citations"})

    @app.route("/create_test_citation/<author>/<title>/<year>/<journal>")
    def create_test_citation(author, title, year, journal):
        add_citation(
            Citation(
                "article",
                generate_cite_key(
                    {"author": author, "title": title, "year": year, "journal": journal}
                ),
                {"author": author, "title": title, "year": year, "journal": journal},
            )
        )

        return jsonify({"message": "created test citation"})

    @app.route("/create_test_citation_with_optional_field")
    def create_test_citation_with_optional_field():
        citation_data = {"author": "Author", "title": "Title", "year": "2000", "journal": "Journal",
                         "volume": "5050"}
        add_citation(
            Citation(
                "article",
                generate_cite_key(
                    citation_data
                ),
                citation_data
            )
        )

        return jsonify({"message": "created test citation"})
