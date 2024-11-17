from collections import defaultdict
from sqlalchemy import text
from config import db
from entities.citation import Citation


def get_citations() -> list[Citation]:
    citations_dict = defaultdict(lambda: {"fields": {}})

    sql = text("SELECT c.id, c.citation_key, c.citation_type, cf.field_name, cf.field_value FROM citations c LEFT JOIN citation_fields cf ON c.id = cf.citation_id")
    result = db.session.execute(sql)
    rows = result.fetchall()

    for row in rows:
        id, citation_key, citation_type, field_name, field_value = row
        citation = citations_dict[citation_key]
        citation["id"] = id
        citation["citation_key"] = citation_key
        citation["citation_type"] = citation_type
        citation["fields"][field_name] = field_value

    citations = [
        Citation(citation_data["citation_type"], citation_data["citation_key"], citation_data["fields"], citation_data["id"])
        for citation_data in citations_dict.values()
    ]

    return citations

def add_citation(citation: Citation):
    sql = text("INSERT INTO citations (citation_type, citation_key) VALUES (:citation_type, :citation_key) RETURNING id")
    result = db.session.execute(sql, { "citation_type": citation.citation_type, "citation_key": citation.citation_key })
    citation_id = result.fetchone()[0]

    for field_name, field_value in citation.fields.items():
        sql = text("INSERT INTO citation_fields (citation_id, field_name, field_value) VALUES (:citation_id, :field_name, :field_value)")
        db.session.execute(sql, { "citation_id": citation_id, "field_name": field_name, "field_value": field_value })

    db.session.commit()