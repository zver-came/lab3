from sqlalchemy import Column, Integer, String,ForeignKey,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

teacher_studen_association = Table(
    'teacher_student', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.student_id')),
    Column('teacher_id', Integer, ForeignKey('teachers.teacher_id'))
)





