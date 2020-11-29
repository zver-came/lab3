import orm
class Group(orm.Base):
    __tablename__='groups'
    group_id=orm.Column(orm.Integer,autoincrement = True,primary_key=True)
    name=orm.Column('name',orm.String(32))
    students=orm.relationship("Student", back_populates='group',cascade='all, delete, delete-orphan')

    def __init__(self, name):
        self.name = name