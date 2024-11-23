from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.citation_repository import get_citations, add_citation, get_citation_by_id, delete_citation_from_db, update_citation_in_db
from entities.citation import Citation
from config import app, test_env

@app.route("/")
def index():
    # Vielä toteuttamatta olevat tyypit
    types_left = ['booklet', 'conference', 'inbook', 'incollection', 'manual', 'masterthesis', 'misc', 'phdthesis', 
                  'proceedings', 'techreport', 'unpublished']
    # Article on defaulttina
    types = ['book', 'inproceedings']

    citations = get_citations()
    return render_template("index.html", citations=citations, types=types) 

@app.route("/create_citation", methods=["POST"])
def citation_creation():
    types = {
        "article": ["author", "title", "journal", "year"],
        "book": ["author", "editor", "title", "publisher", "year"],
        "inproceedings": ["author", "title"]
    }

    citation_type = request.form.get("citation_type")
    key = request.form.get("key")
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
        return redirect(f"/")
    
#Avaa Citation page   
@app.route('/citation/<int:citation_id>')
def citation_details(citation_id):
    citation = get_citation_by_id(citation_id)
    if not citation:
        abort(404)  # Return a 404 page if the citation is not found
    return render_template('citation.html', citation=citation)

#Poista Citation
@app.route('/delete_citation/<int:citation_id>', methods=['POST'])
def delete_citation_route(citation_id):
    try:
        delete_citation_from_db(citation_id) 
        flash("Citation deleted successfully!", "success")
    except Exception as e:
        flash(f"An error occurred while deleting: {e}", "danger")
    return redirect('/')


@app.route("/edit_citation/<int:citation_id>", methods=["GET"])
def edit(citation_id):
    citation = get_citation_by_id(citation_id)
    citation_id = citation_id
    return render_template('edit_citation.html', citation=citation, citation_id=citation_id)

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
        return redirect("/")

    try:
        update_citation_in_db(citation_id, fields)
        return redirect("/")

    except Exception as e:
        flash(f"An error occurred while editing: {e}", "danger")
        return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })