from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import group as g,teacher as t,student as s,subject as sub,teacher_email as te, student_phone as sp
import psycopg2

class Model:
    def __init__(self):
        try:
            engine = create_engine('postgres+psycopg2://postgres:postgres@localhost:5432/database_lab1')
            Session = sessionmaker(bind=engine)
            self.session=Session()
            self.cursor = None
            self.connection = None
            self.connection = psycopg2.connect(user="postgres", password="postgres",
                                               host="127.0.0.1", port="5432", database="database_lab1")
            self.cursor = self.connection.cursor()
        except(Exception, psycopg2.Error) as error:print("Error connection with PostgreSQL", error)

    def __del__(self):
        self.session.close()
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Connection closed")

    #Student command
    def select_item(self,type,value):
        try:
            return self.session.query(type).get(value)
        except Exception as exp:
            print('You have search problem. Detail info: %s' % exp)


    def add_new_item(self,new_item):
        try:
            self.session.add(new_item)
            self.session.commit()
            return new_item
        except Exception as exp:
            print('You have problem with adding item. Detail info: %s' % exp)

    def delete_item(self,item):
        try:
            self.session.delete(item)
            self.session.commit()
        except Exception as exp:
            print('You have problem with delete item. Detail info: %s'%exp)

    def update_item(self):
        try:
            self.session.commit()
        except Exception as exp:
            print('You have problem with update item. Detail info: %s'%exp)

    def add_new_email(self,teacher_id,email):
        teacher = self.select_item(t.Teacher,teacher_id)
        new_email=te.Teacher_email(email,teacher_id)
        try:
            teacher.emails.append(new_email)
            self.session.commit()
            return True
        except:return False

    def add_new_phone(self,student_id,phone_number):
        student = self.select_item(s.Student,student_id)
        new_phone=(sp.Student_phone(phone_number,student_id))
        try:
            student.phones.append(new_phone)
            self.session.commit()
            return True
        except:return False

    def add_new_link(self,student_id,teacher_id):
        teacher=self.select_item(t.Teacher,teacher_id)
        student=self.select_item(s.Student,student_id)
        try:
            teacher.students.append(student)
            self.session.commit()
            return True
        except:return False

    def delete_link(self,student_id,teacher_id):
        teacher = self.select_item(t.Teacher, teacher_id)
        student = self.select_item(s.Student, student_id)
        try:
            i=teacher.students.index(student)
            del teacher.students[i]
            self.session.commit()
            return True
        except:return False

    #SQL query
    def gen_teachers(self, number):
        self.cursor.execute("with info as (insert into teachers (name,surname,subject_id)"
                            "select random_str(3+(random()*7)::int), random_str(3+(random()*7)::int),random_subject_id()"
                            "from generate_series(1,%s) returning teacher_id)"
                            "insert into teacher_email (email,teacher_id)"
                            "select random_email(7), teacher_id  from info" % (number))
        self.connection.commit()

    def gen_teacher_student_link(self):
        self.cursor.execute("INSERT INTO teacher_student(student_id, teacher_id) "
                            "SELECT link.student_id, link.teacher_id FROM "
                            "(select student_id,random_teacher_id() as teacher_id from students,generate_series(1,2)) as link "
                            "left join teacher_student as ts on "
                            "link.student_id=ts.student_id AND ts.teacher_id=link.teacher_id WHERE ts.student_id IS NULL "
                            "GROUP BY (link.student_id, link.teacher_id)")
        self.connection.commit()

    def gen_students(self, number):
        self.cursor.execute("with info as (insert into students (name, surname, group_id)"
                            "select random_str(3+(random() * 7)::int), random_str(3 + (random() * 7)::int),random_group_id()"
                            "from generate_series(1, %s) returning student_id)"
                            "insert into student_phone(phone_number, student_id)"
                            "select random_phone(), student_id from info" % (number))
        self.connection.commit()

    def gen_group(self, number):
        self.cursor.execute(
            "insert into groups (name) (select chr(trunc(65 + random() * 25)::int) || chr(trunc(65 + random() * 25)::int)"
            "|| chr(45) ||trunc(random() * 99)::int from generate_series(1,%s))" % (number))
        self.connection.commit()

    def gen_subject(self, number):
        self.cursor.execute(
            "insert into subjects (name) select random_str(7) from generate_series(1,%s)" % (number))
        self.connection.commit()

    def find(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_student_teachers(self, student_id, query):
        self.cursor.execute(
            "select t.teacher_id, t.name,t.surname,t.subject_id from teachers as t, students as s, teacher_student as ts %s"
            "where s.student_id = %s and s.student_id=ts.student_id and t.teacher_id=ts.teacher_id order by t.teacher_id" % (
            query, student_id))
        return self.cursor.fetchall()

    def get_all_student_subjects(self, student_id, query, params):
        self.cursor.execute(
            "select sub.subject_id, sub.name from teachers as t,subjects as sub, students as st, teacher_student as ts "
            "%s where t.teacher_id=ts.teacher_id and st.student_id = ts.student_id and st.student_id=%s "
            "and t.subject_id=sub.subject_id %s group by sub.subject_id order by sub.subject_id" % (
            query, student_id, params))
        return self.cursor.fetchall()

    def get_all_teacher_students(self, teacher_id, query):
        self.cursor.execute(
            "select s.student_id, s.name,s.surname from teachers as t, students as s, teacher_student as ts %s "
            "where t.teacher_id = %s and s.student_id=ts.student_id and t.teacher_id=ts.teacher_id order by s.student_id" % (
            query, teacher_id))
        return self.cursor.fetchall()