from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import EmployeeModel
from schemas import EmployeeSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db

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
            return employee
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blp.route("/employees")
class EmployeeList(MethodView):
    @blp.response(200, EmployeeSchema(many=True))
    def get(self):
        return EmployeeModel.query.all()
