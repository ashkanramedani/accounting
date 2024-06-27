import pandas as pd
from sqlalchemy import inspect, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine('postgresql://admin:adminadmin@localhost:5432/Acc1')
Session = sessionmaker(bind=engine)
session = Session()
inspector = inspect(engine)
schemas = inspector.get_schema_names()

INVALID_KEYS = ["description", "priority", "visible", "deleted", "can_update", "can_deleted", "create_date", "update_date", "delete_date", "expire_date"]
RES = {}
for table_name in inspector.get_table_names(schema="public"):
    RES[table_name] = []
    for column in inspector.get_columns(table_name, schema="public"):
        if column["name"] not in INVALID_KEYS:
            RES[table_name].append(column["name"])

MAX_l = max([len(l) for l in RES.values()])

for k, v in RES.items():
    while len(v) < MAX_l:
        RES[k].append("")
res = pd.DataFrame.from_dict(RES).to_csv("./TmpFiles/All.csv")
