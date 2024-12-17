from collections import defaultdict
from sqlalchemy import text
from config import db
from entities.citation import Citation


GET_CITATIONS_SQL = text("""
    SELECT c.id, c.citation_key, c.citation_type, cf.field_name, cf.field_value
    FROM citations c LEFT JOIN citation_fields cf ON c.id = cf.citation_id
""")

INSERT_CITATION_SQL = text("""
    INSERT INTO citations (citation_type, citation_key) 
    VALUES (:citation_type, :citation_key) RETURNING id
""")

INSERT_CITATION_FIELD_SQL = text("""
    INSERT INTO citation_fields (citation_id, field_name, field_value)
    VALUES (:citation_id, :field_name, :field_value)
""")

GET_UNIQUE_FIELD_NAMES_SQL = text("""
    SELECT DISTINCT field_name
    FROM citation_fields
    WHERE field_name IS NOT NULL
    ORDER BY field_name ASC
""")

GET_ALL_CITATION_KEYS_SQL = text("""
    SELECT c.citation_key 
    FROM citations c
""")

GET_CITATION_BY_ID_SQL = text("""
    SELECT c.id, c.citation_key, c.citation_type, cf.field_name, cf.field_value 
    FROM citations c 
    LEFT JOIN citation_fields cf ON c.id = cf.citation_id 
    WHERE c.id = :citation_id
""")

DELETE_CITATION_FIELDS_SQL = text("""
    DELETE FROM citation_fields WHERE citation_id = :citation_id
""")

DELETE_CITATION_SQL = text("""
    DELETE FROM citations WHERE id = :citation_id
""")

REMOVE_CITATION_FIELD_SQL = text("""
    DELETE FROM citation_fields
    WHERE citation_id = :citation_id AND field_name = :field_name
""")

GET_CITATION_FIELD_NAMES_SQL = text("""
    SELECT cf.field_name
    FROM citations c LEFT JOIN citation_fields cf ON c.id = cf.citation_id
    WHERE c.id = :citation_id
""")

UPDATE_FIELD_SQL = text("""
    UPDATE citation_fields
    SET field_value = :field_value 
    WHERE citation_id = :citation_id AND field_name = :field_name
""")

INSERT_FIELD_SQL = text("""
    INSERT INTO citation_fields (citation_id, field_name, field_value)
    VALUES (:citation_id, :field_name, :field_value)
""")


def get_citations() -> list[Citation]:
    citations_dict = defaultdict(lambda: {"fields": {}})
    result = db.session.execute(GET_CITATIONS_SQL)
    rows = result.fetchall()

    for row in rows:
        citation_id, citation_key, citation_type, field_name, field_value = row
        citation = citations_dict[citation_key]
        citation["id"] = citation_id
        citation["citation_key"] = citation_key
        citation["citation_type"] = citation_type
        citation["fields"][field_name] = field_value

    citations = [
        Citation(
            citation_data["citation_type"],
            citation_data["citation_key"],
            citation_data["fields"],
            citation_data["id"],
        )
        for citation_data in citations_dict.values()
    ]

    return citations


def add_citation(citation: Citation):
    result = db.session.execute(
        INSERT_CITATION_SQL,
        {
            "citation_type": citation.citation_type,
            "citation_key": citation.citation_key,
        },
    )
    citation_id = result.fetchone()[0]

    for field_name, field_value in citation.fields.items():
        db.session.execute(
            INSERT_CITATION_FIELD_SQL,
            {
                "citation_id": citation_id,
                "field_name": field_name,
                "field_value": field_value,
            },
        )

    db.session.commit()


# Hae viite id:lla
def get_citation_by_id(citation_id: int) -> dict:
    """
    Retrieves a single citation by its ID and returns it as a dictionary.
    """
    result = db.session.execute(GET_CITATION_BY_ID_SQL, {"citation_id": citation_id})
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
        citation_data["id"],
    ).to_dict()


# Poista citation
def delete_citation_from_db(citation_id: int):
    """
    Deletes a citation and its associated fields from the database.
    """
    db.session.execute(DELETE_CITATION_FIELDS_SQL, {"citation_id": citation_id})
    db.session.execute(DELETE_CITATION_SQL, {"citation_id": citation_id})
    db.session.commit()


def remove_citation_field_from_db(citation_id, field_name):
    db.session.execute(REMOVE_CITATION_FIELD_SQL,
                       {"citation_id": citation_id, "field_name": field_name})
    db.session.commit()


def get_citation_field_names(citation_id):
    result = db.session.execute(GET_CITATION_FIELD_NAMES_SQL, {"citation_id": citation_id})
    rows = result.fetchall()
    return {row[0] for row in rows}


def update_citation_in_db(citation_id: int, citation_fields: dict):
    existing_fields = get_citation_field_names(citation_id)

    for field_name, field_value in citation_fields.items():
        if field_name in existing_fields:
            db.session.execute(
                UPDATE_FIELD_SQL,
                {"citation_id": citation_id, "field_name": field_name, "field_value": field_value}
            )
            existing_fields.remove(field_name)
        else:
            db.session.execute(
                INSERT_FIELD_SQL,
                {"citation_id": citation_id, "field_name": field_name, "field_value": field_value}
            )

    for field_name in existing_fields:
        remove_citation_field_from_db(citation_id, field_name)

    db.session.commit()


def unique_key(key):
    result = db.session.execute(GET_ALL_CITATION_KEYS_SQL)
    rows = result.fetchall()
    for existing_key in rows:
        if key == existing_key[0]:
            return False
    return True


def get_unique_field_names() -> set:
    """
    Retrieves a set of all unique field names used across all citations.
    """
    result = db.session.execute(GET_UNIQUE_FIELD_NAMES_SQL)
    rows = result.fetchall()
    return {row[0] for row in rows}
