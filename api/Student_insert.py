from db import models
from db.models import SessionLocal
import pandas as pd

# Initialize database session
db = SessionLocal()

# Get the UNKNOWN_ROLE primary key id
UNKNOWN_ROLE = db.query(models.Role_form).filter_by(deleted=False, name="Unknown", cluster="Users").first().role_pk_id

# Read the Excel file and convert to dictionary
students = pd.read_excel("./IeltsDaily_Student.xlsx").to_dict(orient='records')


# Function to format id and phone numbers
def format_number(number):
    return str(number) if str(number).startswith("0") else f'0{number}'


# Process each student record
for student in students:
    data = {
        'name': student["name"],
        'last_name': student["lastname"],
        'id_card_number': format_number(student["ID card"]),
        'mobile_number': format_number(student["phone"]),
        'email': student["email"]
    }
    print(data)

    # Create and add User_form object to the database
    user = models.User_form(created_fk_by="308e2744-833c-4b94-8e27-44833c2b940f", is_employee=False, **data)  # type: ignore[call-arg]
    db.add(user)
    db.commit()
    db.refresh(user)

    # Append role to the user and commit
    unknown_role = db.query(models.Role_form).filter_by(role_pk_id=UNKNOWN_ROLE, deleted=False).first()
    user.roles.append(unknown_role)
    db.commit()
    db.refresh(user)
