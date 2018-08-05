import click

from datetime import date

from absents import app, db
from absents.domain import Absence, Grade, SchoolClass, Student, Teacher, Vacation


@app.cli.command()
def create_db():
    db.create_all()


@app.cli.command()
def clear_db():
    db.drop_all()


@app.cli.command()
def create_grades():
    db.session.add(Grade(cycle=2, level=1, name='CP'))
    db.session.add(Grade(cycle=2, level=2, name='CE1'))
    db.session.add(Grade(cycle=2, level=3, name='CE2'))
    db.session.add(Grade(cycle=3, level=1, name='CM1'))
    db.session.add(Grade(cycle=3, level=2, name='CM2'))
    db.session.commit()


@app.cli.command()
def create_vacations_2018():
    db.session.add(Vacation(start_date=date(2018, 10, 20), end_date=date(2018, 11, 4)))
    db.session.add(Vacation(start_date=date(2018, 12, 22), end_date=date(2019, 1, 6)))
    db.session.add(Vacation(start_date=date(2019, 2, 9), end_date=date(2019, 2, 24)))
    db.session.add(Vacation(start_date=date(2019, 4, 6), end_date=date(2019, 4, 22)))
    db.session.add(Vacation(start_date=date(2019, 5, 29), end_date=date(2019, 6, 2)))
    db.session.add(Vacation(start_date=date(2019, 7, 6), end_date=date(2019, 9, 1)))
    db.session.commit()


@app.cli.command()
@click.pass_context
def create_test_db(ctx):
    ctx.forward(clear_db)
    ctx.invoke(clear_db)
    ctx.forward(create_db)
    ctx.invoke(create_db)
    ctx.forward(create_grades)
    ctx.invoke(create_grades)
    ctx.forward(create_vacations_2018)
    ctx.invoke(create_vacations_2018)

    the_class = SchoolClass(year=2018)
    ce1 = Grade.query.filter_by(name='CE1').first()
    ce2 = Grade.query.filter_by(name='CE2').first()
    the_class.grades.append(ce1)
    the_class.grades.append(ce2)

    the_class.teachers.append(Teacher(firstname="Géraldine", lastname="Seiler", email="geyraldine@gmail.com"))
    the_class.teachers.append(Teacher(firstname="Fanny", lastname="Thenaut", email="fanny@gmail.com"))

    john = Student(firstname="John", lastname="Doe", schoolclass=the_class, grade=ce1, start_date=date(2018, 9, 3), end_date=date(2018, 12, 24))
    Student(firstname="Jane", lastname="Doe", schoolclass=the_class, grade=ce2, start_date=date(2018, 10, 1), end_date=date(2019, 7, 12))
    Student(firstname="Eli", lastname="Copter", schoolclass=the_class, grade=ce1, start_date=date(2018, 9, 3), end_date=date(2019, 7, 12))
    Student(firstname="Clair", lastname="Delune", schoolclass=the_class, grade=ce2, start_date=date(2018, 9, 3), end_date=date(2019, 7, 12))
    Student(firstname="Jean", lastname="Bon", schoolclass=the_class, grade=ce1, start_date=date(2018, 9, 3), end_date=date(2019, 7, 12))

    db.session.add(the_class)

    db.session.add(Absence(date=date(2018, 9, 4), period='all_day', student=john))
    db.session.commit()
