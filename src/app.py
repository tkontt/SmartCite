from flask import redirect, render_template, request, jsonify, flash, abort
from db_helper import reset_db
from repositories.citation_repository import (
    get_citations,
    add_citation,
    get_citation_by_id,
)
from repositories.citation_repository import remove_citation_field_from_db
from repositories.citation_repository import (
    delete_citation_from_db,
    update_citation_in_db,
    get_unique_field_names,
)
from repositories.tag_repository import get_tags, create_tag, check_if_valid_tag
from entities.citation import Citation
from entities.tag import Tag
from config import app, test_env
from util import (
    generate_cite_key,
    validate_fields,
    generate_bibtex,
    import_bibtex_citations,
    validate_bibtex,
    valid_inputs,
)

TYPES = {
    "article": ["author", "title", "journal", "year"],
    "book": ["author", "editor", "title", "publisher", "year"],
    "inproceedings": ["author", "title"],
    "booklet": ["title"],
    "conference": ["author", "title"],
    "inbook": ["author", "title", "chapter", "publisher", "year"],
    "incollection": ["author", "title", "booktitle"],
    "manual": ["title"],
    "masterthesis": ["author", "title", "school", "year"],
    "misc": [],
    "phdthesis": ["author", "title", "school", "year"],
    "proceedings": ["title", "year"],
    "techreport": ["author", "title", "institution", "year"],
    "unpublished": ["author", "title"],
}


@app.route("/")
def index():
    # Article on defaulttina
    types = [
        "book",
        "inproceedings",
        "booklet",
        "conference",
        "inbook",
        "incollection",
        "manual",
        "masterthesis",
        "misc",
        "phdthesis",
        "proceedings",
        "techreport",
        "unpublished",
    ]

    all_fields = get_unique_field_names()
    default_headers = ["author", "title", "year", "type"]

    citations = get_citations()
    tags = get_tags()

    return render_template(
        "index.html",
        citations=citations,
        types=types,
        tags=tags,
        default_headers=default_headers,
        all_fields=all_fields,
    )


@app.route("/create_citation", methods=["POST"])
def citation_creation():
    citation_type = request.form.get("citation-type")
    fields = {}
    all_fields = request.form.get("all-fields-new").split(",")

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


# Avaa Citation page
@app.route("/citation/<int:citation_id>")
def citation_details(citation_id):
    citation = get_citation_by_id(citation_id)
    if not citation:
        abort(404)  # Return a 404 page if the citation is not found
    return render_template("citation.html", citation=citation, citation_id=citation_id)


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
    all_fields = request.form.get("all-fields-edit").split(",")
    fields = {}

    if all_fields == [""]:
        delete_citation_from_db(citation_id)
        flash("Citation removed due to all fields being removed.")
        return redirect("/")

    for field in all_fields:
        fields[field] = request.form.get(field).strip()

    if "" in fields.values():
        flash("Missing required fields")
        return redirect(f"/citation/{citation_id}")

    try:
        update_citation_in_db(citation_id, fields)
        return redirect(f"/citation/{citation_id}")

    except Exception as e:
        flash(f"An error occurred while editing: {e}", "danger")
        return redirect(f"/citation/{citation_id}")


@app.route("/create_tag", methods=["POST"])
def tag_creation():
    tag = request.form.get("tag").lower()
    if check_if_valid_tag(tag):
        try:
            tag_create = Tag(tag)
            create_tag(tag_create)
            return redirect("/")
        except Exception as error:
            flash(str(error))
            return redirect("/")
    else:
        error = Exception("Tag needs to between 1 and 7 characters long.")
        flash(str(error))
        return redirect("/")


@app.route("/create_bibtex", methods=["GET"])
def create_bibtex():
    citations = get_citations()
    return generate_bibtex(citations)


@app.route("/import_citations_bibtex", methods=["POST"])
def import_from_bibtex():
    bibtex = request.form.get("input_bibtex")
    try:
        validate_bibtex(bibtex)
    except Exception as error:
        flash(str(error))
        return redirect("/")

    citations = import_bibtex_citations(bibtex)

    for c in citations:
        add_citation(c)
    try:
        valid_inputs(bibtex, citations)
        flash(f"{len(citations)} citation/s added successfully!")
    except Exception as error:
        flash(str(error))
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


@app.route("/remove_citation_field/<citation_id>/<field_name>", methods=["POST"])
def remove_citation_field(citation_id, field_name):
    remove_citation_field_from_db(citation_id, field_name)

    return {"result": "success"}
