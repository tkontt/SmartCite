from flask import redirect, render_template, request, jsonify, flash, abort
from db_helper import reset_db
from repositories.citation_repository import get_citations, add_citation, get_citation_by_id, delete_citation_from_db, update_citation_in_db
from repositories.tag_repository import get_tags, create_tag, delete_tag_from_db, check_if_valid_tag
from entities.citation import Citation
from entities.tag import Tag
from config import app, test_env
from util import generate_cite_key

@app.route("/")
def index():
    # Vielä toteuttamatta olevat tyypit
    types_left = ['booklet', 'conference', 'inbook', 'incollection',
                  'manual', 'masterthesis', 'misc', 'phdthesis',
                  'proceedings', 'techreport', 'unpublished']
    # Article on defaulttina
    types = ['book', 'inproceedings']

    citations = get_citations()
    tags = get_tags()
    return render_template("index.html", citations=citations, types=types, tags=tags)

@app.route("/create_citation", methods=["POST"])
def citation_creation():
    types = {
        "article": ["author", "title", "journal", "year"],
        "book": ["author", "editor", "title", "publisher", "year"],
        "inproceedings": ["author", "title"]
    }

    citation_type = request.form.get("citation_type")
    key = generate_cite_key()
    fields = {}

    for field in types[citation_type]:
        fields[field] = request.form.get(field).strip()

    if "" in fields.values():
        flash("Missing required fields")
        return redirect("/")

    try:
        citation = Citation(citation_type, key, fields)
        add_citation(citation)

        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/")

#Avaa Citation page
@app.route('/citation/<int:citation_id>')
def citation_details(citation_id):
    citation = get_citation_by_id(citation_id)
    if not citation:
        abort(404)  # Return a 404 page if the citation is not found
    return render_template('citation.html', citation=citation, citation_id=citation_id)

#Poista Citation
@app.route('/delete_citation/<int:citation_id>', methods=['POST'])
def delete_citation_route(citation_id):
    try:
        delete_citation_from_db(citation_id)
        flash("Citation deleted successfully!", "success")
    except Exception as e:
        flash(f"An error occurred while deleting: {e}", "danger")
    return redirect('/')

#Muokkaa
@app.route('/update_citation', methods=['POST'])
def edit_citation_form_route():
    types = {
        "article": ["author", "title", "journal", "year"],
        "book": ["author", "editor", "title", "publisher", "year"],
        "inproceedings": ["author", "title"]
    }

    citation_id = request.form.get("citation_id")
    citation_type = request.form.get("citation_type")

    fields = {}

    for field in types[citation_type]:
        fields[field] = request.form.get(field)

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

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
