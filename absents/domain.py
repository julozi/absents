from absents import db


schoolclass_grade = db.Table('schoolclass_grade',
                             db.Column('schoolclasse_id', db.Integer, db.ForeignKey('schoolclass.id'), primary_key=True),
                             db.Column('grade_id', db.Integer, db.ForeignKey('grade.id'), primary_key=True))

schoolclass_teacher = db.Table('schoolclass_teacher',
                               db.Column('schoolclasse_id', db.Integer, db.ForeignKey('schoolclass.id'), primary_key=True),
                               db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'), primary_key=True))


class SchoolYear(db.Model):
    __tablename__ = 'schoolyear'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)


class SchoolClass(db.Model):
    __tablename__ = 'schoolclass'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, db.ForeignKey('schoolyear.id'), nullable=False)
    room = db.Column(db.String, nullable=False)
    bilingual = db.Column(db.Boolean, nullable=False, default=False)

    grades = db.relationship('Grade', secondary=schoolclass_grade, lazy='subquery', backref=db.backref('grades', lazy=True))
    teachers = db.relationship('Teacher', secondary=schoolclass_teacher, lazy='subquery', backref=db.backref('teacehrs', lazy=True))
    schoolyear = db.relationship(SchoolYear)

    @property
    def name(self):
        teachears = " / ".join(["%s. %s" % (teacher.firstname[0], teacher.lastname) for teacher in self.teachers])
        name = "Salle %s" % self.room
        if teachears:
            name = "%s (%s)" % (name, teachears)
        return name

    @property
    def grade(self):
        return " / ".join([grade.name for grade in self.grades])


class Grade(db.Model):
    __tablename__ = 'grade'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cycle = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, nullable=False)


class Teacher(db.Model):
    __tablename__ = 'teacher'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    gender = db.Column(db.Enum('m', 'f', name='student_gender'), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)

    schoolclass_id = db.Column(db.Integer, db.ForeignKey('schoolclass.id', ondelete='CASCADE'))
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    schoolclass = db.relationship(SchoolClass, backref="students")
    grade = db.relationship(Grade)

    def __repr__(self):
        return "%s %s" % (self.firstname, self.lastname)

    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'grade': self.grade_id,
            'start_date': self.start_date,
            'end_date': self.end_date
        }


class Absence(db.Model):
    __tablename__ = 'absence'

    SYMBOL = {
        'morning': '&#8212;',
        'afternoon': '|',
        'all_day': '+'
    }

    SCORE = {
        'morning': 0.5,
        'afternoon': 0.5,
        'all_day': 1.0
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    period = db.Column(db.Enum('morning', 'afternoon', 'all_day', name='absence_period'), nullable=False)
    reason = db.Column(db.Text, nullable=True)

    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'))

    student = db.relationship(Student)

    @property
    def symbol(self):
        return self.SYMBOL[self.period]

    @property
    def score(self):
        return self.SCORE[self.period]


class Vacation(db.Model):
    __tablename__ = 'vacation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
