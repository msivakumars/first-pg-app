import redis, os
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import EmployeeModel
from schemas import EmployeeSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from task import send_user_registration_email, send_email
from rq import Queue


blp = Blueprint("Employee", "employee", description="Operations for Employee")


@blp.route("/employee")
class CreateEmployee(MethodView):
    @blp.arguments(EmployeeSchema)
    @blp.response(201, EmployeeSchema)
    def post(self, employee_data):
        employee = EmployeeModel(**employee_data)
        try:
            db.session.add(employee)
            db.session.commit()
            to = employee_data["email_id"]
            subject = f"Employee data created for {employee_data['firstname']} {employee_data['lastname']} "
            body= f" Welcome {employee_data['firstname']} to ZeMoSo Technology."
            # send_simple_message(to, subject=subject, body=body)
            fullname = f"{employee_data['firstname']} {employee_data['lastname']} "
            redis_connection = redis.from_url(os.getenv("REDIS_URL"))
            queue = Queue("emails", connection=redis_connection)
            queue.enqueue(send_user_registration_email, email_id=to, username=fullname)
            # send_email(to=to], sub=subject, body=body)
            return employee
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blp.route("/employees")
class EmployeeList(MethodView):
    @blp.response(200, EmployeeSchema(many=True))
    def get(self):
        return EmployeeModel.query.all()


# import requests, os
# from dotenv import load_dotenv
# def send_simple_message(to, subject, body):
#     load_dotenv()
#     domain = os.getenv("MAILGUN_DOMAIN")
#     return requests.post(
#     f"https://api.mailgun.net/v3/{domain}/messages",
#     auth=("api", os.getenv("MAILGUN_API_KEY")),
#     data={"from": f"Sivakumar M <mailgun@{domain}>",
#         "to": [to],
#         "subject": subject,
#         "text": body})
