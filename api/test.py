from sqlalchemy import or_, Float, Integer, String, Boolean
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
try:
    from os import getenv
    from time import sleep
    from typing import List, cast
    from pathlib import Path
    from json import dump, load
    from dotenv import load_dotenv
    from datetime import datetime, timedelta, timezone

    # DB
    from redis import asyncio as redis
    from sqlalchemy.exc import OperationalError

    # fastApi
    from fastapi import FastAPI
    from fastapi_limiter import FastAPILimiter
    from contextlib import asynccontextmanager
    from fastapi.middleware.cors import CORSMiddleware

except (ImportError, ModuleNotFoundError):
    raise Exception('Requirement Not Satisfied: some_module is missing')

from router import routes
from lib import logger
from db import models, save_route, setUp_admin, engine, SessionLocal, Create_Redis_URL

config = load(open("configs/config.json"))


# Replace these details with your database configuration
DATABASE_URL = "postgresql://admin:adminadmin@localhost:5432/Acc1"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def Validate(column, SearchKey):
    name = column.name
    column_type = column.type
    if "_pk_" in name or "_fk_" in name:
        return False

    if name in ['priority', 'visible', 'deleted', 'can_update', 'can_deleted', 'create_date', 'update_date', 'delete_date', 'expire_date', 'status', 'description']:
        return False
    if isinstance(column_type, String):
        column.like(f'%{SearchKey}%')
    elif isinstance(column_type, (Integer, Float)):
        cast(column, String).like(f'%{SearchKey}%')
    elif isinstance(column_type, Boolean):
        if SearchKey.lower() in ["true", "1"]:
            column.is_(True)
        elif SearchKey.lower() in ["false", "0"]:
            return column.is_(False)
    return False


def search_keyword_in_table(table_name, keyword):
    table = models.User_form
    columns = table.__table__.columns
    like_conditions = []
    for column in columns:
        c = Validate(column, keyword)
        if c:
            like_conditions.append(c)

    query = session.query(table).filter(or_(*like_conditions))

    print(query)
    results = query.all()
    return results


results = search_keyword_in_table("user", "Ad")

for result in results:
    print(result)

"""
SELECT "user".priority AS user_priority, "user".visible AS user_visible, "user".deleted AS user_deleted, "user".can_update AS user_can_update, "user".can_deleted AS user_can_deleted, "user".create_date AS user_create_date, "user".update_date AS user_update_date, "user".delete_date AS user_delete_date, "user".expire_date AS user_expire_date, "user".status AS user_status, "user".description AS user_description, "user".note AS user_note, "user".user_pk_id AS user_user_pk_id, "user".created_fk_by AS user_created_fk_by, "user".name AS user_name, "user".last_name AS user_last_name, "user".nickname AS user_nickname, "user".day_of_birth AS user_day_of_birth, "user".email AS user_email, "user".mobile_number AS user_mobile_number, "user".emergency_number AS user_emergency_number, "user".id_card_number AS user_id_card_number, "user".address AS user_address, "user".fingerprint_scanner_user_id AS user_fingerprint_scanner_user_id, "user".is_employee AS user_is_employee, "user".level AS user_level 
FROM "user" 
WHERE "user".name LIKE %(name_1)s OR "user".last_name LIKE %(last_name_1)s OR "user".nickname LIKE %(nickname_1)s OR "user".email LIKE %(email_1)s OR "user".mobile_number LIKE %(mobile_number_1)s OR "user".emergency_number LIKE %(emergency_number_1)s OR "user".id_card_number LIKE %(id_card_number_1)s OR "user".address LIKE %(address_1)s OR "user".fingerprint_scanner_user_id LIKE %(fingerprint_scanner_user_id_1)s OR "user".level LIKE %(level_1)s

"""
