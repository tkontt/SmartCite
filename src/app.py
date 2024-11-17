from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.todo_repository import get_todos, create_todo, set_done
from repositories.citation_repository import get_citations
from config import app, test_env
from util import validate_todo

@app.route("/")
def index():
    citations = get_citations()
    return render_template("index.html", citations=citations) 

@app.route("/new_citation")
def new():
    return render_template("new_citation.html")

@app.route("/create_citation", methods=["POST"])
def citation_creation():
    citation_type = request.form.get("citation_type")
    content = request.form.get("content")
    author = request.form.get("author/s")

    try:
        # tämä ei vielä tehty
        # create_citation(citation_type, author, content)
        
        validate_todo(content)
        create_todo(content)

        return redirect("/")
    except Exception as error:
        flash(str(error))
        return  redirect("/new_citation")

@app.route("/toggle_todo/<todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    set_done(todo_id)
    return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
