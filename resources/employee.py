from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import EmployeeModel
from schemas import EmployeeSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
import requests, os
from dotenv import load_dotenv
from resources.email import send_email

blp = Blueprint("Employee", "employee", description="Operations for Employee")


def send_simple_message(to, subject, body):
    load_dotenv()
    domain = os.getenv("MAILGUN_DOMAIN")
    return requests.post(
    f"https://api.mailgun.net/v3/{domain}/messages",
    auth=("api", os.getenv("MAILGUN_API_KEY")),
    data={"from": f"Sivakumar M <mailgun@{domain}>",
        "to": [to],
        "subject": subject,
        "text": body})

@blp.route("/employee")
class CreateEmployee(MethodView):
    @blp.arguments(EmployeeSchema)
    @blp.response(201, EmployeeSchema)
    def post(self, employee_data):
        employee = EmployeeModel(**employee_data)
        try:
            db.session.add(employee)
            db.session.commit()
            subject = f"Employee data created for {employee_data['firstname']} {employee_data['lastname']} "
            body= f" Welcome {employee_data['firstname']} to ZeMoSo Technology."
            send_simple_message(to=employee_data["email_id"], subject=subject, body=body)
            send_email(to=employee_data["email_id"], sub=subject, body=body)
            return employee
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blp.route("/employees")
class EmployeeList(MethodView):
    @blp.response(200, EmployeeSchema(many=True))
    def get(self):
        return EmployeeModel.query.all()


