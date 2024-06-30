from db import db
from sqlalchemy import Column, String, Integer


class EmployeeModel(db.Model):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True)
    firstname = Column(String(80),  nullable=False)
    lastname = Column(String(80),  nullable=False)
    email_id = Column(String(80), unique=False, nullable=True)
