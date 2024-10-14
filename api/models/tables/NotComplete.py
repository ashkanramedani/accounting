from sqlalchemy import BigInteger
from sqlalchemy.orm import relationship

from .Base_form import *


class Department(Base):
    __tablename__ = 'tbl_departments'
    department_pk_id = Column(BigInteger, nullable=False, autoincrement=True, unique=True, primary_key=True, index=True)


class EducationalInstitutions(Base, Base_form):
    __tablename__ = "tbl_educational_institutions"

    educational_institution_pk_id = Column(BigInteger, nullable=False, autoincrement=True, unique=True, primary_key=True, index=True)
    educational_institution_name = Column(String(100), unique=True, nullable=False)
    educational_institution_hash = Column(String(100), unique=True)

    def __repr__(self):
        return f'<EducationalInstitution "{self.educational_institution_pk_id}">'


class Class_Room:  # NC: 008
    pass


class Branch:  # NC: 008
    pass


# class Reassign_Instructor_form(Base, Base_form):
#     __tablename__ = "reassign_instructor"
#
#     reassign_instructor_pk_id = create_Unique_ID()
#     created_fk_by = create_forenKey("User_form")
#     sessions_fk_id = create_forenKey("Session_form")
#     main_teacher_fk_id = create_forenKey("User_form")
#     sub_teacher_fk_id = create_forenKey("User_form")
#
#     created = relationship("User_form", foreign_keys=[created_fk_by])
#     sessions = relationship("Session_form", foreign_keys=[sessions_fk_id])
#     main_teacher = relationship("User_form", foreign_keys=[main_teacher_fk_id])
#     sub_teacher = relationship("User_form", foreign_keys=[sub_teacher_fk_id])
#
# class Survey_form(Base, Base_form):
#     __tablename__ = "survey"
#     survey_pk_id = create_Unique_ID()
#     sub_course_fk_id = create_foreignKey("Sub_Course_form")
#     created_fk_by = create_foreignKey("User_form")
#     title = Column(String, index=True)
#
#     created = relationship("User_form", foreign_keys=[created_fk_by])
#     sub_course = relationship("Sub_Course_form", foreign_keys=[sub_course_fk_id])
#     questions = relationship('Question_form', secondary=survey_questions, backref='surveys')
#
#     def __repr__(self):
#         return Remove_Base_Data(self.__dict__)
#
#
# class Question_form(Base, Base_form):
#     __tablename__ = "question"
#     question_pk_id = create_Unique_ID()
#     created_fk_by = create_foreignKey("User_form")
#     text = Column(String, unique=True)
#     language = Column(String, index=True)
#
#     created = relationship("User_form", foreign_keys=[created_fk_by])
#
#     def __repr__(self):
#         return Remove_Base_Data(self.__dict__)
#
#
# class Response_form(Base, Base_form):
#     __tablename__ = "response"
#     response_pk_id = create_Unique_ID()
#     user_fk_id = create_foreignKey("User_form")
#     question_fk_id = create_foreignKey("Question_form")
#     survey_fk_id = create_foreignKey("Survey_form")
#     answer = Column(String, nullable=False)
#
#     student = relationship("User_form", foreign_keys=[user_fk_id])
#     question = relationship("Question_form", foreign_keys=[question_fk_id])
#     survey = relationship("Survey_form", foreign_keys=[survey_fk_id])
#
#     # Roles
#
#     def __repr__(self):
#         return Remove_Base_Data(self.__dict__)
