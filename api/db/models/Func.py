from fastapi_utils.guid_type import GUID as GUID_TYPE, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table, BigInteger, MetaData, Float, UniqueConstraint, DATE, TIME, Date, Time
from sqlalchemy.dialects.postgresql import JSONB, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression, func

from .database import Base

# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

metadata_obj = MetaData()


class GUID(GUID_TYPE):
    cache_ok = True




def create_Unique_ID():
    return Column(GUID, server_default=GUID_SERVER_DEFAULT_POSTGRESQL, primary_key=True, nullable=False, unique=True, index=True)


def create_forenKey(table: str, unique: bool = False, index: bool = False, nullable: bool = False):
    table_name = table.lower().replace("_form", "")
    return Column(GUID, ForeignKey(f'{table_name}.{table_name + "_pk_id"}', ondelete="CASCADE"), nullable=nullable, unique=unique, index=index)

Modes_relation = {
    "created": "created_fk_by",
    "student": "student_fk_id"
}


def relation(table: str, relation_title: str = "created"):
    return relationship(table, back_populates=relation_title, foreign_keys=f"{table}.{Modes_relation[relation_title]}")
