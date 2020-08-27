import click
import csv

from datetime import date, datetime

from absents import app, db
from absents.domain import Absence, Grade, SchoolClass, SchoolYear, Student, Teacher, Vacation


@app.cli.command()
def create_db():
    db.create_all()
    db.session.commit()


@app.cli.command()
def clear_db():
    db.drop_all()
    db.session.commit()


@app.cli.command()
def create_grades():
    db.session.add(Grade(cycle=2, level=1, name='CP'))
    db.session.add(Grade(cycle=2, level=2, name='CE1'))
    db.session.add(Grade(cycle=2, level=3, name='CE2'))
    db.session.add(Grade(cycle=3, level=1, name='CM1'))
    db.session.add(Grade(cycle=3, level=2, name='CM2'))
    db.session.commit()


@app.cli.command()
def create_2018():
    db.session.add(SchoolYear(id=2018, start_date=date(2018, 9, 3), end_date=date(2019, 7, 5)))
    # Vacances scolaires
    db.session.add(Vacation(start_date=date(2018, 10, 20), end_date=date(2018, 11, 4)))
    db.session.add(Vacation(start_date=date(2018, 12, 22), end_date=date(2019, 1, 6)))
    db.session.add(Vacation(start_date=date(2019, 2, 9), end_date=date(2019, 2, 24)))
    db.session.add(Vacation(start_date=date(2019, 4, 6), end_date=date(2019, 4, 22)))
    db.session.add(Vacation(start_date=date(2019, 5, 29), end_date=date(2019, 6, 2)))
    db.session.add(Vacation(start_date=date(2019, 7, 6), end_date=date(2019, 9, 1)))
    # Toussaint
    db.session.add(Vacation(start_date=date(2018, 11, 1), end_date=date(2018, 11, 1)))
    # Armistice
    db.session.add(Vacation(start_date=date(2018, 11, 11), end_date=date(2018, 11, 11)))
    # Noel
    db.session.add(Vacation(start_date=date(2018, 12, 25), end_date=date(2018, 12, 25)))
    # Jour de l'an
    db.session.add(Vacation(start_date=date(2019, 1, 1), end_date=date(2019, 1, 1)))
    # Epiphanie
    db.session.add(Vacation(start_date=date(2019, 1, 6), end_date=date(2019, 1, 6)))
    # Lundi de Paques
    db.session.add(Vacation(start_date=date(2019, 4, 22), end_date=date(2019, 4, 22)))
    # Fête du travail
    db.session.add(Vacation(start_date=date(2019, 5, 1), end_date=date(2019, 5, 1)))
    # Victoire 1945
    db.session.add(Vacation(start_date=date(2019, 5, 8), end_date=date(2019, 5, 8)))
    # Ascension
    db.session.add(Vacation(start_date=date(2019, 5, 30), end_date=date(2019, 5, 30)))
    # Lundi de Pentecôte
    db.session.add(Vacation(start_date=date(2019, 6, 10), end_date=date(2019, 6, 10)))
    db.session.commit()


@app.cli.command()
def create_2019():
    db.session.add(SchoolYear(id=2019, start_date=date(2019, 9, 2), end_date=date(2020, 7, 4)))
    # Vacances scolaires
    db.session.add(Vacation(start_date=date(2019, 10, 19), end_date=date(2019, 11, 3)))  # Toussaint
    db.session.add(Vacation(start_date=date(2019, 12, 21), end_date=date(2020, 1, 5)))  # Noël
    db.session.add(Vacation(start_date=date(2020, 2, 15), end_date=date(2020, 3, 1)))  # Hiver
    db.session.add(Vacation(start_date=date(2020, 4, 11), end_date=date(2020, 4, 26)))  # Printemps
    db.session.add(Vacation(start_date=date(2020, 5, 22), end_date=date(2020, 5, 23)))  # Pont
    db.session.add(Vacation(start_date=date(2020, 7, 4), end_date=date(2020, 8, 31)))  # Ete
    # Toussaint
    db.session.add(Vacation(start_date=date(2019, 11, 1), end_date=date(2019, 11, 1)))
    # Armistice
    db.session.add(Vacation(start_date=date(2019, 11, 11), end_date=date(2019, 11, 11)))
    # Noel
    db.session.add(Vacation(start_date=date(2019, 12, 25), end_date=date(2019, 12, 25)))
    # Jour de l'an
    db.session.add(Vacation(start_date=date(2020, 1, 1), end_date=date(2020, 1, 1)))
    # Epiphanie
    db.session.add(Vacation(start_date=date(2020, 1, 6), end_date=date(2020, 1, 6)))
    # Lundi de Paques
    db.session.add(Vacation(start_date=date(2020, 4, 13), end_date=date(2020, 4, 13)))
    # Fête du travail
    db.session.add(Vacation(start_date=date(2020, 5, 1), end_date=date(2020, 5, 1)))
    # Victoire 1945
    db.session.add(Vacation(start_date=date(2020, 5, 8), end_date=date(2020, 5, 8)))
    # Ascension
    db.session.add(Vacation(start_date=date(2020, 5, 21), end_date=date(2020, 5, 21)))
    # Lundi de Pentecôte
    db.session.add(Vacation(start_date=date(2020, 5, 31), end_date=date(2020, 5, 31)))
    db.session.commit()


@app.cli.command()
def create_2020():
    db.session.add(SchoolYear(id=2020, start_date=date(2020, 9, 1), end_date=date(2021, 7, 6)))
    # Vacances scolaires
    db.session.add(Vacation(start_date=date(2020, 10, 17), end_date=date(2020, 11, 1)))  # Toussaint
    db.session.add(Vacation(start_date=date(2020, 12, 19), end_date=date(2021, 1, 3)))  # Noël
    db.session.add(Vacation(start_date=date(2021, 2, 20), end_date=date(2021, 3, 7)))  # Hiver
    db.session.add(Vacation(start_date=date(2021, 4, 24), end_date=date(2021, 5, 9)))  # Printemps
    db.session.add(Vacation(start_date=date(2021, 5, 13), end_date=date(2021, 5, 15)))  # Pont
    db.session.add(Vacation(start_date=date(2021, 7, 7), end_date=date(2021, 8, 31)))  # Ete
    # Toussaint
    db.session.add(Vacation(start_date=date(2020, 11, 1), end_date=date(2020, 11, 1)))
    # Armistice
    db.session.add(Vacation(start_date=date(2020, 11, 11), end_date=date(2020, 11, 11)))
    # Noel
    db.session.add(Vacation(start_date=date(2020, 12, 25), end_date=date(2020, 12, 25)))
    # Jour de l'an
    db.session.add(Vacation(start_date=date(2021, 1, 1), end_date=date(2021, 1, 1)))
    # Vendredi saint
    db.session.add(Vacation(start_date=date(2021, 4, 2), end_date=date(2021, 4, 2)))
    # Lundi de Paques
    db.session.add(Vacation(start_date=date(2021, 4, 5), end_date=date(2021, 4, 5)))
    # Fête du travail
    db.session.add(Vacation(start_date=date(2021, 5, 1), end_date=date(2021, 5, 1)))
    # Victoire 1945
    db.session.add(Vacation(start_date=date(2021, 5, 8), end_date=date(2021, 5, 8)))
    # Ascension
    db.session.add(Vacation(start_date=date(2021, 5, 13), end_date=date(2021, 5, 13)))
    # Lundi de Pentecôte
    db.session.add(Vacation(start_date=date(2021, 5, 24), end_date=date(2021, 5, 24)))
    db.session.commit()


@app.cli.command()
@click.option('--year', type=click.INT)
@click.argument('f', type=click.Path(exists=True))
def import_csv(year, f):
    school_year = SchoolYear.query.get(year)

    with open(f, 'r') as csvfile:
        students = csv.reader(csvfile, delimiter=';')
        for student_data in students:
            room = student_data[0]
            try:
                int(room)
            except ValueError:
                print("Ignoring line : %s" % student_data)
                continue
            school_class = SchoolClass.query.filter_by(room=room).filter_by(schoolyear=school_year).first()
            if not school_class:
                bilingual = student_data[2] == 'X'
                school_class = SchoolClass(schoolyear=school_year, room=room, bilingual=bilingual)
                db.session.add(school_class)

            grade = Grade.query.filter_by(name=student_data[1]).first()
            if grade is None:
                print("Can't find grade for line : %s" % student_data)
                continue

            if grade not in school_class.grades:
                school_class.grades.append(grade)

            choral = student_data[3] == 'X'
            ulis = student_data[4] == 'X'
            student = Student(firstname=student_data[6],
                              lastname=student_data[5],
                              birth_date=datetime.strptime(student_data[7], '%d/%m/%Y').date(),
                              gender=student_data[8].lower(),
                              start_date=school_year.start_date,
                              end_date=school_year.end_date,
                              ulis=ulis,
                              choral=choral,
                              schoolclass=school_class,
                              grade=grade)
            db.session.add(student)
            db.session.commit()


@app.cli.command()
@click.pass_context
def create_test_db(ctx):
    ctx.forward(clear_db)
    ctx.forward(create_db)
    ctx.forward(create_grades)
    ctx.forward(create_2018)

    ce1 = Grade.query.filter_by(name='CE1').first()
    ce2 = Grade.query.filter_by(name='CE2').first()
    schoolyear = SchoolYear.query.get(2018)

    the_class = SchoolClass(schoolyear=schoolyear, room=109, bilingual=True)
    the_class.grades.append(ce1)
    the_class.grades.append(ce2)
    the_class.teachers.append(Teacher(firstname="Géraldine", lastname="Seiler", email="geyraldine@gmail.com"))
    the_class.teachers.append(Teacher(firstname="Fanny", lastname="Thenaut", email="fanny@gmail.com"))

    john = Student(firstname="John", lastname="Doe", gender='m', birth_date=date(2010, 1, 1), schoolclass=the_class, grade=ce1, start_date=schoolyear.start_date, end_date=date(2018, 12, 24))
    Student(firstname="Jane", lastname="Doe", gender='f', birth_date=date(2010, 1, 1), schoolclass=the_class, grade=ce2, start_date=date(2018, 10, 1), end_date=schoolyear.end_date)
    Student(firstname="Eli", lastname="Copter", gender='m', birth_date=date(2010, 1, 1), schoolclass=the_class, grade=ce1, start_date=schoolyear.start_date, end_date=schoolyear.end_date)
    Student(firstname="Claire", lastname="Delune", gender='f', birth_date=date(2010, 1, 1), schoolclass=the_class, grade=ce2, start_date=schoolyear.start_date, end_date=schoolyear.end_date, ulis=True)
    Student(firstname="Jean", lastname="Bon", gender='m', birth_date=date(2010, 1, 1), schoolclass=the_class, grade=ce1, start_date=schoolyear.start_date, end_date=schoolyear.end_date)

    db.session.add(the_class)

    the_class = SchoolClass(schoolyear=schoolyear, room=202, bilingual=False)
    the_class.grades.append(ce1)
    db.session.add(the_class)

    db.session.add(Absence(date=date(2018, 9, 4), period='all_day', student=john))
    db.session.commit()
