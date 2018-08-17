from datetime import date
from flask import Blueprint, flash, redirect, render_template, request, url_for
from good import All, Coerce, Date, Entire, In, Length, Msg, Required, Schema
from good.schema.errors import Invalid, MultipleInvalid

from absents import db
from absents.domain import SchoolClass, Student

bp_students = Blueprint('students', __name__)


def get_student_schema(schoolclass):
    def start_before_end():
        def validator(d):
            if 'start_date' not in d or 'end_date' not in d:
                assert False, "La date d'arrivée dans la classe ou la date de départ ne sont pas renseignées"
            if not isinstance(d['start_date'], date) or not isinstance(d['end_date'], date):
                assert False, "La date d'arrivée dans la classe ou la date de départ ne sont pas conformes"
            assert d['start_date'] <= d['end_date'], "La date d'arrivée dans la classe doit être antérieur à la date de départ"

            return d
        return validator

    schema = Schema({
        'firstname': Msg(Length(min=1), "Le prénom doit être renseigné."),
        'lastname': Msg(Length(min=1), "Le nom doit être renseigné."),
        'grade': All(
            Coerce(int),
            Msg(In([grade.id for grade in schoolclass.grades]),
                "Le niveau choisi n'est pas disponible pour cette classe.")),
        'start_date': Msg(Date('%d/%m/%Y'), "La date d'arrivée dans la classe doit être renseignée."),
        'end_date': Msg(Date('%d/%m/%Y'), "La date de départ de la classe doit être renseignée."),
        Entire: start_before_end()
        }, default_keys=Required)

    return schema


@bp_students.route('/<int:class_id>/students', methods=['GET'])
def list(class_id):
    schoolclass = SchoolClass.query.get(class_id)
    students = Student.query.filter_by(schoolclass=schoolclass)\
                            .order_by(Student.lastname, Student.firstname)\
                            .all()
    return render_template('students/list.html',
                           schoolclass=schoolclass,
                           students=students)


@bp_students.route('/<int:class_id>/students/new', methods=['GET'])
def new(class_id):
    schoolclass = SchoolClass.query.get(class_id)
    return render_student_form(schoolclass)


def render_student_form(schoolclass, student=None):
    student = student if student is not None else {}
    if isinstance(student, Student):
        student = student.to_dict()
    print(student)
    if 'start_date' in student:
        if isinstance(student['start_date'], date):
            student['start_date'] = student['start_date'].strftime('%d/%m/%Y')
    if 'end_date' in student:
        if isinstance(student['end_date'], date):
            student['end_date'] = student['end_date'].strftime('%d/%m/%Y')
    return render_template('students/new.html',
                           schoolclass=schoolclass,
                           student=student)


@bp_students.route('/<int:class_id>/students', methods=['POST'])
def add(class_id):
    schoolclass = SchoolClass.query.get(class_id)
    data = request.form.to_dict()

    student_schema = get_student_schema(schoolclass)

    try:
        student_schema(data)
    except Invalid as error:
        if isinstance(error, MultipleInvalid):
            errors = error
        else:
            errors = [error]

        for invalid in errors:
            if isinstance(invalid.validator, Required):
                flash("Une erreur inattendue s'est produite. Merci de \
                contacter l'administrateur de l'application.", 'danger')
            else:
                flash(invalid.message, 'warning')
        return render_student_form(schoolclass, data)

    student = Student(
        firstname=data['firstname'],
        lastname=data['lastname'],
        grade_id=data['grade'],
        start_date=data['start_date'],
        end_date=data['end_date'])
    schoolclass.students.append(student)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        flash("Une erreur s'est produite lors de l'enregistrement de l'élève. \
        Merci de contacter l'administrateur de l'application.", 'danger')
        return redirect(url_for('students.list', class_id=class_id))

    flash("Elève enregistré avec succès", 'success')
    return redirect(url_for('students.list', class_id=class_id))
