from fastapi_utils.guid_type import GUID as GUID_TYPE, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import Column, ForeignKey, MetaData
from sqlalchemy.orm import relationship

# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

metadata_obj = MetaData()


class GUID(GUID_TYPE):
    cache_ok = True


def create_Unique_ID():
    return Column(GUID, server_default=GUID_SERVER_DEFAULT_POSTGRESQL, primary_key=True, nullable=False, unique=True, index=True)


def create_foreignKey(table: str, unique: bool = False, index: bool = True, nullable: bool = False):
    table_name = table.lower().replace("_form", "")
    return Column(GUID, ForeignKey(f'{table_name}.{table_name + "_pk_id"}', ondelete="CASCADE"), nullable=nullable, unique=unique, index=index)


def creator_relation(table: str):
    """
    Create a relationship with creator. (Did not used in new version)
    args:
        table: table name
    """
    return relationship(table, back_populates="created", foreign_keys=f"{table}.created_fk_by", cascade="all, delete-orphan")
