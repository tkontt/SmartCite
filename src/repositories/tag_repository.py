from collections import defaultdict
from sqlalchemy import text
from config import db
from entities.tag import Tag


def get_tags() -> list[Tag]:
    tags_dict = defaultdict(lambda: {"fields": {}})

    sql = text("SELECT id, tag FROM tags")
    result = db.session.execute(sql)
    rows = result.fetchall()

    for row in rows:
        tag_id, tag_name = row
        tag = tags_dict[tag_name]
        tag["id"] = tag_id
        tag["name"] = tag_name

    tags = [
        Tag(tag_data["name"], tag_data["id"])
        for tag_data in tags_dict.values()
    ]

    return tags


def create_tag(tag: Tag):
    sql = text("INSERT INTO tags (tag) VALUES (:tag_name) RETURNING id")
    db.session.execute(sql, { "tag_name": tag.tag })
    db.session.commit()

def delete_tag_from_db(tag_id: int):
    sql_delete_tag = text("DELETE FROM tags WHERE id = :tag_id")
    db.session.execute(sql_delete_tag, { "tag_id": tag_id})
    db.session.commit()

def check_if_valid_tag(tag):
    if 0 < len(tag) and len(tag) <= 7:
        return True
    return False
