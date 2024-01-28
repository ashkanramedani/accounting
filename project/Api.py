from fastapi import FastAPI, Depends, responses, Response, HTTPException
import Models
import Validation
from Connector import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from loguru import logger
from json import load
from os.path import dirname, join


Config = load(open("./Config.json", 'r'))

api = FastAPI()
Models.PSQL.metadata.create_all(bind=engine)

logger.add(sink=join(dirname(__file__), Config["Logger"]["File"]["Path"]),
           rotation=Config["Logger"]["File"]["Size"],
           format=Config["Logger"]["Format"],
           level="INFO")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


dependency = Annotated[Session, Depends(get_db)]


@api.post("/add_employee/")
async def add_employee(employee: Validation.BASE_Employee, db: dependency, response: Response):
    try:
        OBJ = Models.Employee(
                name=employee.name,
                last_name=employee.last_name,
                job_title=employee.job_title)

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200
    except Exception as error:
        logger.error(error)
        return 500


@api.get("/")
async def root(response: Response):
    logger.info(response.status_code)
    return 200



@api.post("/search_employee")
async def search_employee(employee_id: int, db: dependency):
    res = db.query(Models.Employee).filter(Models.Employee.id == employee_id).all()

    logger.info(res)
    if not res:
        return {"status_code": 200, "res": "NotFound"}
    return {"status_code": 200, "res": res}



@api.post("/Form/")
async def form(Form: Validation.BASE_Leave_Form, db: dependency):
    db.query(Models.Employee).filter(Models.Employee.id == Form.id)
    OBJ = Models.Leave_form(
            id=Form.id,
            employee_id=Form.employee_id,
            Start_Date=Form.start,
            End_Date=Form.end,
            Description=Form.Description
    )
    db.add(OBJ)
    db.commit()
    db.refresh(OBJ)

