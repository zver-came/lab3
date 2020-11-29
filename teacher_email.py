import orm
class Teacher_email(orm.Base):
    __tablename__='teacher_email'
    email=orm.Column('email',orm.String(50),primary_key=True)
    teacher_id = orm.Column(orm.Integer,orm.ForeignKey('teachers.teacher_id'),primary_key=True)
    teacher=orm.relationship('Teacher',back_populates='emails')

    def __init__(self, email,teacher_id):
        self.email=email
        self.teacher_id=teacher_id