from sqlalchemy.exc import SQLAlchemyError

from db.models import User, Advertisement, Region, Category
from db.mysql import MySQL
from config.config import conf

mysql = MySQL(**conf)


def create_user(**values):
    try:
        mysql.insert(User, **values)
        return 201
    except SQLAlchemyError as e:
        return 400, e


def create_advertisement(**values):
    try:
        mysql.insert(Advertisement, **values)
        return 201
    except SQLAlchemyError as e:
        return 400, e


def create_region(**values):
    try:
        mysql.insert(Region, **values)
        return 201
    except SQLAlchemyError as e:
        return 400, e


def update_user(username, **values):
    try:
        table_obj = User.__table__
        id = mysql.query(table_obj.columns.id).filter(table_obj.columns.username == username).scalar()
        if not id:
            return 404, None
        mysql.update(User, id, **values)
        user = mysql.query(table_obj).filter(table_obj.columns.id == id).one_or_none()
        user_response = dict(zip(table_obj.columns.keys(), user))
        return 200, user_response
    except SQLAlchemyError as e:
        return 400, e


def update_advertisement(id, **values):
    try:
        mysql.update(Advertisement, id, **values)
        table_obj = Advertisement.__table__
        advertisement = mysql.query(table_obj).filter(table_obj.columns.id == id).one_or_none()
        if not advertisement:
            return 404, None
        advertisement_response = dict(zip(table_obj.columns.keys(), advertisement))
        return 200, advertisement_response
    except SQLAlchemyError as e:
        return 400, e


def get_all_advertisements():
    try:
        res = mysql.select(Advertisement)
        return 200, res
    except SQLAlchemyError as e:
        return 400, e


def get_all_advertisements_by_region(id):
    try:
        clause = Advertisement.__table__.columns.region_id == id
        return 200, mysql.select(Advertisement, where=clause)
    except SQLAlchemyError as e:
        return 400, e


def get_user_by_username(username):
    try:
        clause = User.__table__.columns.username == username
        return 200, mysql.select(User, where=clause)[0]
    except SQLAlchemyError as e:
        return 500, e


def get_region(id):
    try:
        clause = Region.__table__.columns.id == id
        response = mysql.select(Region, where=clause)[0]
        print(response)
        return response
    except SQLAlchemyError as e:
        return 400, e


def delete_advertisement_by_id(id):
    try:
        mysql.delete(Advertisement, id)
        return 200
    except SQLAlchemyError as e:
        return 400, str(e)

#######################################


def check_if_record_in_db(table_model, id):
    try:
        return mysql.check_if_record_in_db(table_model, id)
    except SQLAlchemyError as e:
        return e


def get_all_id(table_model):
    table_obj = table_model.__table__
    return [res[0] for res in mysql.query(table_obj.columns.id).all()]


def get_all_usernames():
    table_obj = User.__table__
    return [res[0] for res in mysql.query(table_obj.columns.username).all()]