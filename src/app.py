from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.citation_repository import get_citations, add_citation, get_citation_by_id, delete_citation_from_db
from entities.citation import Citation
from config import app, test_env

@app.route("/")
def index():
    citations = get_citations()
    return render_template("index.html", citations=citations) 


@app.route("/new_citation")
def new():
    types = ['book', 'booklet', 'conference', 'inbook', 'incollection', 'inproceedings',
            'manual', 'masterthesis', 'misc', 'phdthesis', 'proceedings', 'techreport', 'unpublished']

    return render_template("new_citation.html", types=types)

@app.route("/create_citation", methods=["POST"])
def citation_creation():
    citation_type = request.form.get("citation_type")
    key = request.form.get("key")
    title = request.form.get("title")
    author = request.form.get("author")
    year = request.form.get("year")
    publisher = request.form.get("publisher")

    if not title or not author or not year or not publisher:
        flash("Missing required fields")
        return redirect("/new_citation")

    try:
        citation = Citation(citation_type, key, {"title": title, "author": author, "year": year, "publisher": publisher})
        add_citation(citation)

        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect(f"/new_citation")
    
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

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })