import orm

class Teacher(orm.Base):
    __tablename__='teachers'
    teacher_id=orm.Column(orm.Integer,autoincrement = True,primary_key=True)
    name=orm.Column('name',orm.String(50))
    surname=orm.Column('surname',orm.String(50))
    subject_id=orm.Column(orm.Integer,orm.ForeignKey('subjects.subject_id'))
    students = orm.relationship("Student", secondary=orm.teacher_studen_association)
    emails=orm.relationship("Teacher_email",back_populates='teacher',cascade='all, delete, delete-orphan')
    subject=orm.relationship("Subject",back_populates='teachers')

    def __init__(self, name,surname,subject_id):
        self.name=name
        self.surname = surname
        self.subject_id=subject_id
