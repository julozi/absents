from datetime import date
from flask import abort, Blueprint, flash, redirect, render_template, request, url_for
from good import All, Any, Coerce, Date, Entire, In, Length, Msg, Optional, Range, Required, Schema
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
                assert False
            assert d['start_date'] <= d['end_date'], "La date d'arrivée dans la classe doit être antérieur à la date de départ"

            return d
        return validator

    schema = Schema({
        'firstname': Msg(Length(min=1), "Le prénom doit être renseigné."),
        'lastname': Msg(Length(min=1), "Le nom doit être renseigné."),
        Optional('birth_date'): Any('', Msg(Date('%d/%m/%Y'), "La date de naissance doit être renseignée.")),
        'gender': Msg(Any('f', 'm'), "Vous devez sélectionner une valeur pour le sexe"),
        'grade': All(
            Coerce(int),
            Msg(In([grade.id for grade in schoolclass.grades]),
                "Le niveau choisi n'est pas disponible pour cette classe.")),
        'start_date': All(
            Msg(Date('%d/%m/%Y'), "La date d'arrivée dans la classe doit être renseignée."),
            Msg(Range(schoolclass.schoolyear.start_date, schoolclass.schoolyear.end_date),
                "La date d'arrivée dans la classe doit être comprise entre le %s et le %s" % (schoolclass.schoolyear.start_date.strftime("%d/%m/%Y"), schoolclass.schoolyear.end_date.strftime("%d/%m/%Y")))),
        'end_date': All(
            Msg(Date('%d/%m/%Y'), "La date de départ de la classe doit être renseignée."),
            Msg(Range(schoolclass.schoolyear.start_date, schoolclass.schoolyear.end_date),
                "La date de départ de la classe doit être comprise entre le %s et le %s" % (schoolclass.schoolyear.start_date.strftime("%d/%m/%Y"), schoolclass.schoolyear.end_date.strftime("%d/%m/%Y")))),
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


def render_student_form(schoolclass, student=None):
    student = student if student is not None else {}
    if isinstance(student, Student):
        student = student.to_dict()

    date_fields = ('birth_date', 'start_date', 'end_date')
    for date_field in date_fields:
        if date_field in student and isinstance(student[date_field], date):
            student[date_field] = student[date_field].strftime('%d/%m/%Y')

    template = 'students/new.html'
    if 'id' in student:
        template = 'students/edit.html'

    return render_template(template,
                           schoolclass=schoolclass,
                           student=student)


def handle_validation_error(error):
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


@bp_students.route('/<int:class_id>/students/new', methods=['GET'])
def new(class_id):
    schoolclass = SchoolClass.query.get(class_id)
    return render_student_form(schoolclass)


@bp_students.route('/<int:class_id>/students', methods=['POST'])
def add(class_id):
    schoolclass = SchoolClass.query.get(class_id)
    data = request.form.to_dict()

    student_schema = get_student_schema(schoolclass)

    try:
        student_schema(data)
    except Invalid as error:
        handle_validation_error(error)
        return render_student_form(schoolclass, data)

    student = Student(
        firstname=data['firstname'],
        lastname=data['lastname'],
        gender=data['gender'],
        grade_id=data['grade'],
        start_date=data['start_date'],
        end_date=data['end_date'])
    if 'birth_date' in data and isinstance(data['birth_date'], date):
        student.birth_date = data['birth_date']
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


@bp_students.route('/<int:class_id>/students/<int:student_id>', methods=['GET'])
def edit(class_id, student_id):
    student = Student.query.get(student_id)
    if student is None:
        abort(404)

    if student.schoolclass_id != class_id:
        abort(500)

    return render_student_form(student.schoolclass, student)


@bp_students.route('/<int:class_id>/students/<int:student_id>', methods=['PUT'])
def update(class_id, student_id):
    schoolclass = SchoolClass.query.get(class_id)
    data = request.form.to_dict()
    student_schema = get_student_schema(schoolclass)

    try:
        student_schema(data)
    except Invalid as error:
        handle_validation_error(error)
        return render_student_form(schoolclass, data)

    student = Student.query.get(student_id)
    student.firstname = data['firstname']
    student.lastname = data['lastname']
    student.gender = data['gender']
    student.grade_id = data['grade']
    student.start_date = data['start_date']
    student.end_date = data['end_date']

    if 'birth_date' in data and isinstance(data['birth_date'], date):
        student.birth_date = data['birth_date']
    else:
        student.birth_date = None

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        flash("Une erreur s'est produite lors de l'enregistrement de l'élève. \
        Merci de contacter l'administrateur de l'application.", 'danger')
        return redirect(url_for('students.list', class_id=class_id))

    flash("Elève modifié avec succès", 'success')
    return redirect(url_for('students.list', class_id=class_id))


@bp_students.route('/<int:class_id>/students/<int:student_id>', methods=['DELETE'])
def delete(class_id, student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()

    flash("Elève supprimé avec succès", 'success')
    return redirect(url_for('students.list', class_id=class_id))
