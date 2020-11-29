import orm

class Subject(orm.Base):
    __tablename__='subjects'
    name=orm.Column('name',orm.String(50))
    subject_id=orm.Column(orm.Integer,autoincrement = True,primary_key=True)
    teachers = orm.relationship("Teacher", back_populates='subject', cascade='all, delete, delete-orphan')

    def __init__(self, name,):
        self.name=name