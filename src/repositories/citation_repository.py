from collections import defaultdict
from sqlalchemy import text
from config import db
from entities.citation import Citation


def get_citations() -> list[Citation]:
    citations_dict = defaultdict(lambda: {"fields": {}})

    sql = text("""SELECT c.id, c.citation_key, c.citation_type, cf.field_name, cf.field_value
               FROM citations c LEFT JOIN citation_fields cf ON c.id = cf.citation_id
               """)
    result = db.session.execute(sql)
    rows = result.fetchall()

    for row in rows:
        citation_id, citation_key, citation_type, field_name, field_value = row
        citation = citations_dict[citation_key]
        citation["id"] = citation_id
        citation["citation_key"] = citation_key
        citation["citation_type"] = citation_type
        citation["fields"][field_name] = field_value

    citations = [
        Citation(citation_data["citation_type"],
                 citation_data["citation_key"],
                 citation_data["fields"],
                 citation_data["id"])
        for citation_data in citations_dict.values()
    ]

    return citations

def add_citation(citation: Citation):
    sql = text("""
               INSERT INTO citations (citation_type, citation_key) 
               VALUES (:citation_type, :citation_key) RETURNING id
               """)
    result = db.session.execute(sql, { "citation_type": citation.citation_type,
                                      "citation_key": citation.citation_key })
    citation_id = result.fetchone()[0]

    for field_name, field_value in citation.fields.items():
        sql = text("""
                   INSERT INTO citation_fields (citation_id, field_name, field_value)
                   VALUES (:citation_id, :field_name, :field_value)
                   """)
        db.session.execute(sql, { "citation_id": citation_id,
                                 "field_name": field_name,
                                 "field_value": field_value })

    db.session.commit()

#Hae viite id:lla
def get_citation_by_id(citation_id: int) -> dict:
    """
    Retrieves a single citation by its ID and returns it as a dictionary.
    """
    sql = text("""
        SELECT c.id, c.citation_key, c.citation_type, cf.field_name, cf.field_value 
        FROM citations c 
        LEFT JOIN citation_fields cf ON c.id = cf.citation_id 
        WHERE c.id = :citation_id
    """)
    result = db.session.execute(sql, {"citation_id": citation_id})
    rows = result.fetchall()

    if not rows:
        return None

    citation_data = {"fields": {}}
    for row in rows:
        citation_id, citation_key, citation_type, field_name, field_value = row
        citation_data["id"] = citation_id
        citation_data["citation_key"] = citation_key
        citation_data["citation_type"] = citation_type
        if field_name:
            citation_data["fields"][field_name] = field_value

    return Citation(
        citation_data["citation_type"],
        citation_data["citation_key"],
        citation_data["fields"],
        citation_data["id"]
    ).to_dict()

#Poista citation
def delete_citation_from_db(citation_id: int):
    """
    Deletes a citation and its associated fields from the database.
    """
    sql_delete_fields = text("DELETE FROM citation_fields WHERE citation_id = :citation_id")
    sql_delete_citation = text("DELETE FROM citations WHERE id = :citation_id")

    db.session.execute(sql_delete_fields, {"citation_id": citation_id})
    db.session.execute(sql_delete_citation, {"citation_id": citation_id})
    db.session.commit()


def update_citation_in_db(citation_id: int, citation_fields: dict):
    for field_name, field_value in citation_fields.items():
        sql_update_field = text("""
                                UPDATE citation_fields SET field_value = :field_value 
                                WHERE citation_id = :citation_id AND field_name = :field_name
                                """)
        db.session.execute(
            sql_update_field,
            {"citation_id": citation_id, "field_name": field_name, "field_value": field_value}
        )
    db.session.commit()

def unique_key(key):
    sql = text("SELECT c.citation_key FROM citations c")
    result = db.session.execute(sql)
    rows = result.fetchall()
    print(rows)
    if key in rows:
        return False
    return True
