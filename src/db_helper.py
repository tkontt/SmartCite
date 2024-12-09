from sqlalchemy import text
from config import db, app

CITATIONS_TABLE = "citations"
CITATION_FIELDS_TABLE = "citation_fields"

def table_exists(name):
    sql_table_existence = text(
        "SELECT EXISTS ("
        "    SELECT 1"
        "    FROM information_schema.tables"
        f"   WHERE table_name = '{name}'"
        ")"
    )

    print(f"Checking if table {name} exists")
    print(sql_table_existence)

    result = db.session.execute(sql_table_existence)
    return result.fetchall()[0][0]




def reset_db():
    clear_table(CITATIONS_TABLE)
    clear_table(CITATION_FIELDS_TABLE)




def clear_table(table_name: str):
    print(f"Clearing contents from table {table_name}")
    sql = text(f"DELETE FROM {table_name}")
    db.session.execute(sql)
    db.session.commit()




def setup_db():
    drop_table_if_exists(CITATIONS_TABLE)
    drop_table_if_exists(CITATION_FIELDS_TABLE)

    sql = text(
        f"CREATE TABLE {CITATIONS_TABLE} ("
        "    id SERIAL PRIMARY KEY, "
        "    citation_type TEXT NOT NULL,"
        "    citation_key TEXT NOT NULL UNIQUE"
        ");"
        f"CREATE TABLE {CITATION_FIELDS_TABLE} ("
        "    id SERIAL PRIMARY KEY, "
        f"   citation_id INT REFERENCES {CITATIONS_TABLE} (id) ON DELETE CASCADE,"
        "    field_name TEXT NOT NULL,"
        "    field_value TEXT NOT NULL,"
        "    UNIQUE (citation_id, field_name)"
        ")"
    )
    db.session.execute(sql)
    db.session.commit()




def drop_table_if_exists(table_name: str):
    if table_exists(table_name):
        print(f"Table {table_name} exists, dropping")
        sql = text(f"DROP TABLE {table_name} CASCADE")
        db.session.execute(sql)
        db.session.commit()




if __name__ == "__main__":
    with app.app_context():
        setup_db()
