import orm
class Student_phone(orm.Base):
    __tablename__='student_phone'
    phone_number=orm.Column('phone_number',orm.String(50),primary_key=True)
    student_id=orm.Column(orm.Integer,orm.ForeignKey('students.student_id'),primary_key=True)
    student=orm.relationship('Student',back_populates='phones')

    def __init__(self, phone_number,student_id):
        self.phone_number=phone_number
        self.student_id=student_id