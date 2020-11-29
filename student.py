import orm
class Student(orm.Base):
    __tablename__='students'
    student_id=orm.Column(orm.Integer,autoincrement = True,primary_key=True)
    name=orm.Column('name',orm.String(50))
    surname=orm.Column('surname',orm.String(50))
    group_id=orm.Column(orm.Integer,orm.ForeignKey('groups.group_id'))
    teachers=orm.relationship("Teacher", secondary=orm.teacher_studen_association)
    phones=orm.relationship('Student_phone',back_populates='student',cascade='all, delete, delete-orphan')
    group=orm.relationship('Group',back_populates='students')

    def __init__(self, name,surname,group_id):
        self.name=name
        self.surname = surname
        self.group_id=group_id