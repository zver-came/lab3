from view import View
from model import Model
import group as g,teacher as t,student as s,subject as sub,teacher_email as te, student_phone as sp
from time import time
from item_search import Search
search=Search()
database=Model()
view=View()

class Controller:
    def __init__(self):
        self.the_student={}
        self.the_teacher={}

    def check_item(self):
        while 1:
            id = input("Enter id:")
            if id.isnumeric():
                if int(id) > 0:
                    return int(id)
            else:
                print("Don't enter id: %s" % id)

    def item_select_function(self, function, element, find):
        while 1:
            print("-------------------------------------------")
            print("1. find %s\n2. enter %s id\n3. exit" % (element, element))
            input_line = input("Enter command: ").strip()
            if input_line.isnumeric():
                input_line = int(input_line)
                if (input_line == 1):
                    input_line = find()
                    function(input_line)
                elif (input_line == 2):
                    self.cheack_id(function)
                elif (input_line == 3):
                    break
                else:
                    print("Try again")
            else:
                print("Please don`t enter this %s id -> (%s)" % (element, input_line))

    def cheack_id(self, function):
        while 1:
            id = input("Enter id:").strip()
            if id.isnumeric():
                function(int(id))
                break
            else:
                print("Don't enter id: %s" % id)

    def cheack_human(self, item, type):
        print("Enter %s params:" % type)
        while 1:
            item['name'] = input("Name: ").strip()
            if len(item['name']) == 0:
                print("Name is empty")
            else:
                break
        while 1:
            item['surname'] = input("Surname: ").strip()
            if len(item['surname']) == 0:
                print("Surname is empty")
            else:
                return item

    def find_student(self):
        search.student_params()
        start_time = time()
        students = database.find(search.create_query())
        finish_time = time() - start_time
        view.print_items(students)
        print("request execution time: %s" % finish_time,
              "\n----------------------------------------------------------------------")
        id = self.check_item()
        for student in students:
            if (student[0] == id):
                return id
        print("Student with id = (%s) is not included in the list of found students" % id)
        return 0

    def find_teacher(self):
        search.teacher_params()
        start_time = time()
        teachers = database.find(search.create_query())
        finish_time = time() - start_time
        view.print_items(teachers)
        print("request execution time: %s" % finish_time,
              "\n----------------------------------------------------------------------")
        id = self.check_item()
        for teacher in teachers:
            if (teacher[0] == id):
                return id
        print("Teacher with id = (%s) is not included in the list of found teachers" % id)
        return 0
    # student menu
    def add_new_student(self):
        self.the_student = self.cheack_human(self.the_student, "student")
        search.find_group()
        groups = database.find(search.create_query())
        view.print_items(groups)
        self.the_student['group'] = False
        while not self.the_student['group']:
            id = self.check_item()
            for group in groups:
               if (group[0] == id):
                    self.the_student['group'] = id
                    break
        new_student = s.Student(self.the_student['name'],self.the_student['surname'], self.the_student['group'])
        view.create_item('Student', database.add_new_item(new_student).student_id)

    def print_student(self, student_id):
        student=database.select_item(s.Student,student_id)
        if student:
            view.print_string('ID: %s\tName: %s\tSurname: %s\tGroup: %s'
                              %(student_id,student.name,student.surname,student.group.name))
            if (student.phones):
                for phone in student.phones:
                    print(phone.phone_number)
        else:view.not_found('Student')

    def print_student_by_id(self):self.item_select_function(self.print_student, "student", self.find_student)

    def delete_student(self, student_id):
        student = database.select_item(s.Student,student_id)
        if (student):
            database.delete_item(student)
            view.delete_item('Student', student_id)
        else:view.not_found('Student')

    def delete_student_by_id(self):self.item_select_function(self.delete_student, "student", self.find_student)

    def update_student(self, student_id):
        student = database.select_item(s.Student,student_id)
        if student:
            self.the_student['id'] = student_id
            print("Enter params:")
            while 1:
                self.the_student['name'] = input("Name: ").strip()
                if len(self.the_student['name']) == 0: self.the_student['name'] = student.name
                break
            while 1:
                self.the_student['surname'] = input("Surname: ").strip()
                if len(self.the_student['surname']) == 0: self.the_student['surname'] = student.surname
                break
            search.find_group()
            groups = database.find(search.create_query())
            view.print_items(groups)
            self.the_student['group'] = student.group_id
            id = input("Enter id:").strip()
            if len(id) != 0 and id.isnumeric():
                for group in groups:
                    if (group[0] == int(id)):
                        self.the_student['group'] = int(id)
                        break
            student.name=self.the_student['name']
            student.surname=self.the_student['surname']
            student.group_id=self.the_student['group']
            database.update_item()
            view.update_item('Student',student_id)
        else:view.not_found('Student')

    def update_student_by_id(self):self.item_select_function(self.update_student, "student", self.find_student)

    def get_all_student_subject(self, student_id):
        student= database.select_item(s.Student,student_id)
        if student:
            query = ""
            input_line = input("Enter y to set subject parameters: ")
            if (input_line == 'y'):
                search.find_subject()
                query = search.create_query()
            start_time = time()
            if len(query) != 0:subjects = database.get_all_student_subjects(student_id, "natural join (" + query + ") as l"
                                                                            ,"  and  l.subject_id=sub.subject_id ")
            else:subjects = database.get_all_student_subjects(student_id, query, "")
            final_time = time() - start_time
            view.print_items(subjects)
            print("request execution time: ", final_time)
        else:view.not_found('Student')

    def get_all_student_by_id_subject(self):self.item_select_function(self.get_all_student_subject, "student",self.find_student)

    def get_all_student_teacher(self, student_id):
        student=database.select_item(s.Student, student_id)
        if student:
            query = ""
            input_line = input("Enter y to set teacher parameters: ")
            if (input_line == 'y'):
                search.teacher_params()
                query = search.create_query()
            start_time = time()
            if len(query) != 0:
                teachers = database.get_all_student_teachers(student_id, "natural join (" + query + ") as l ")
                final_time = time() - start_time
                view.print_items(teachers)
            else:
                final_time = time() - start_time
                for teacher in student.teachers:
                    self.print_teacher(teacher.teacher_id)
            print("request execution time: ", final_time)
        else:view.not_found('Student')

    def get_all_student_by_id_teacher(self):self.item_select_function(self.get_all_student_teacher, "student",self.find_student)

    def add_new_phone(self, student_id):
        student = database.select_item(s.Student,student_id)
        if student:
            while 1:
                phone = input("Enter new phone: ")
                if len(phone) != 0:
                    try:
                        if (database.add_new_phone(student_id, phone)):
                            view.create_phone(phone)
                        else:
                            print('Phone already exist')
                    except Exception as a:print(a)
                    break
                else:print("Name is empty")
        else:view.not_found('Student')

    def add_new_phone_for_student(self):self.item_select_function(self.add_new_phone, "student", self.find_student)

    def delete_phone(self, student_id):
        student = database.select_item(s.Student,student_id)
        if student:
            while 1:
                phone = input("Enter phone: ")
                if len(phone) != 0:
                    for item in student.phones:
                        if (item.phone_number == phone):
                            database.delete_item(item)
                            view.delete_phone_email('Student phone', phone)
                            return
                    view.not_found('Student phone')
                    break
                else:print("Name is empty")
        else:view.not_found('Student')

    def delete_phone_for_student(self):self.item_select_function(self.delete_phone, "student", self.find_student)

    def update_phone(self, student_id):
        if database.select_item(s.Student,student_id):
            number = input("Enter phone number: ").strip()
            while len(number) == 0:
                print("phone is empty")
                number = input("Enter phone number: ").strip()
            new_number = input("Enter new phone: ").strip()
            while len(new_number) == 0:
                print("phone is empty")
                new_number = input("Enter new phone: ").strip()
            phone=database.select_item(sp.Student_phone,(number,student_id))
            if(phone):
                phone.phone_number=new_number
                database.update_item()
            else:print("Phone isn`t exist")
        else:view.not_found('Student')

    def update_phone_for_student(self):self.item_select_function(self.update_phone, "student", self.find_student)

    def add_new_teacher(self):
        self.the_teacher = self.cheack_human(self.the_teacher, "teacher")
        search.find_subject()
        subjects = database.find(search.create_query())
        view.print_items(subjects)
        self.the_teacher['subject'] = False
        if(subjects):
            while not self.the_teacher['subject']:
                id = self.check_item()
                for subject in subjects:
                    if (subject[0] == id):
                        self.the_teacher['subject'] = id
                        break
            teacher=t.Teacher(self.the_teacher['name'],self.the_teacher['surname'],self.the_teacher['subject'])
            view.create_item('Teacher', database.add_new_item(teacher).teacher_id)
        else:print('Subject don`t exist')

    def print_teacher(self, teacher_id):
        teacher=database.select_item(t.Teacher,teacher_id)
        if teacher:
            view.print_string('ID: %s\tName: %s\tSurname: %s\tSubject: %s'
                                     %(teacher_id,teacher.name,teacher.surname,teacher.subject.name))
            if(teacher.emails):
                for email in teacher.emails:
                    print(email.email)
        else:print("Teacher with id: %s not found" % teacher_id)

    def print_teacher_by_id(self):self.item_select_function(self.print_teacher, "teacher", self.find_teacher)

    def delete_teacher(self, teacher_id):
        teacher = database.select_item(t.Teacher,teacher_id)
        if (teacher):
            database.delete_item(teacher)
            view.delete_item('Teacher', teacher_id)
        else:view.not_found('Teacher')

    def delete_teacher_by_id(self):self.item_select_function(self.delete_teacher, "teacher", self.find_teacher)

    def update_tracher(self, teacher_id):
        teacher = database.select_item(t.Teacher,teacher_id)
        if teacher:
            self.the_teacher['id'] = teacher_id
            print("Enter teacher params:")
            while 1:
                self.the_teacher['name'] = input("Name: ").strip()
                if len(self.the_teacher['name']) == 0: self.the_teacher['name'] = teacher[0][1]
                break
            while 1:
                self.the_teacher['surname'] = input("Surname: ").strip()
                if len(self.the_teacher['surname']) == 0: self.the_teacher['surname'] = teacher[0][2]
                break
            search.find_subject()
            subjects = database.find(search.create_query())
            view.print_items(subjects)
            self.the_teacher['subject'] = teacher[0][3]
            id = input("Enter id:").strip()
            if len(id) != 0 and id.isnumeric():
                for subject in subjects:
                    if (subject[0] == int(id)):
                        self.the_teacher['subject'] = int(id)
                        break
            teacher.name=self.the_teacher['name']
            teacher.surname=self.the_teacher['surname']
            teacher.subject=self.the_teacher['subject']
            database.update_item()
        else:view.not_found('Teacher')

    def update_teacher_by_id(self):self.item_select_function(self.update_tracher, "teacher", self.find_teacher)

    def get_all_teacher_students(self, teacher_id):
        teacher=database.select_item(t.Teacher,teacher_id)
        if teacher:
            query = ""
            input_line = input("Enter y to set student parameters: ")
            if (input_line == 'y'):
                search.student_params()
                query = search.create_query()
            start_time = time()
            if len(query) != 0:students = database.get_all_teacher_students(teacher_id, "natural join (" + query + ") as l ")
            else:students = database.get_all_teacher_students(teacher_id, query)
            final_time = time() - start_time
            view.print_items(students)
            print("request execution time: ", final_time)
        else:view.not_found('Teacher')

    def get_all_teacher_by_id_students(self):self.item_select_function(self.get_all_teacher_students, "teacher",self.find_teacher)

    def add_new_email(self, teacher_id):
        teacher = database.select_item(t.Teacher,teacher_id)
        if teacher:
            while 1:
                email = input("Enter new email: ")
                if len(email) != 0:
                    database.add_new_email(teacher.teacher_id, email)
                    view.create_email(email)
                    break
                else:print("Name is empty")
        else:view.not_found('Teacher')

    def add_new_email_for_teacher(self):self.item_select_function(self.add_new_email, "teacher", self.find_teacher)

    def delete_email(self, teacher_id):
        teacher=database.select_item(t.Teacher,teacher_id)
        if teacher:
            while 1:
                email = input("Enter email adress: ").strip()
                if(len(email)>0):
                    for item in teacher.emails:
                        if (item.email == email):
                            database.delete_item(item)
                            view.delete_phone_email('Teacher email', email)
                            return
                    view.not_found('Teacher email')
                else:print('Empty value')
        else:view.not_found('Teacher')

    def delete_email_for_teacher(self):self.item_select_function(self.delete_email, "teacher", self.find_teacher)

    def update_email(self, teacher_id):
        if database.select_item(t.Teacher,teacher_id):
            number1 = input("Enter old email adress: ").strip()
            while len(number1) == 0:
                print("Email is empty")
                number1 = input("Enter old email adress: ").strip()
            number2 = input("Enter new email adress: ").strip()
            while len(number2) == 0:
                print("Email is empty")
                number2 = input("Enter new email adress: ").strip()
            email=database.select_item(te.Teacher_email,(number1,teacher_id))
            if(email):
                email.email=number2
                database.update_item()
            else:print("Email isn`t exist")
        else:view.not_found('Teacher')

    def update_email_for_teacher(self):self.item_select_function(self.update_email, "teacher", self.find_teacher)

    def add_new_group(self):
        while 1:
            number = input("Enter group name:")
            if len(number) != 0:
                view.create_item('Group',database.add_new_item(g.Group(number)).group_id)
                break
            else:print("Name is empty")

    def delete_group_by_id(self):
        group_id = self.check_item()
        group = database.select_item(g.Group,group_id)
        if (group):
            database.delete_item(group)
            view.delete_item('Group', group.group_id)
        else:view.not_found('Group')

    def update_group(self):
        group_id = self.check_item()
        group=database.select_item(g.Group,group_id)
        if group:
            number = input("Enter group name:").strip()
            while 1:
                if len(number) != 0:
                    group.name = number
                    database.update_item()
                    break
                else:print("Name is empty")
        else:view.not_found('Group')

    def add_new_subject(self):
        while 1:
            number = input("Enter subject name:")
            if len(number) != 0:
                new_subject = sub.Subject(number)
                view.create_item('Subject', database.add_new_item(new_subject).subject_id)
                break
            else:print("Name is empty")

    def delete_subject_by_id(self):
        subject_id = self.check_item()
        subject = database.select_item(sub.Subject,subject_id)
        if (subject):
            database.delete_item(subject)
            view.delete_item('Subject', subject.subject_id)
        else:view.not_found('Subject')

    def update_subject(self):
        subject_id = self.check_item()
        subject=database.select_item(sub.Subject,subject_id)
        if subject:
            while 1:
                number = input("Enter new subject name:")
                if len(number) != 0:
                    subject.name=number
                    database.update_item()
                    break
                else:print("Name is empty")
        else:view.not_found('Student')

    def get_all_subject_teachers(self):
        search.find_subject()
        view.print_items(database.find(search.create_query()))
        subject_id = self.check_item()
        subject=database.select_item(sub.Subject,subject_id)
        if subject:
            for teacher in subject.teachers:
                self.print_teacher(teacher.teacher_id)
        else:view.not_found('Subject')

    def add_new_student_teacher_link(self):
        student_id = self.find_student()
        if database.select_item(s.Student,student_id):
            teacher_id = self.find_teacher()
            if database.select_item(t.Teacher,teacher_id):
                if(database.add_new_link(student_id,teacher_id)):
                    view.create_link(teacher_id,student_id)
                else:print('Link already exist')
            else:view.not_found('Teacher')
        else:view.not_found('Student')

    def delete_student_teacher_link(self):
        student_id = self.find_student()
        if database.select_item(s.Student,student_id):
            teacher_id = self.find_teacher()
            if database.select_item(t.Teacher,teacher_id):
                if (database.delete_link(student_id, teacher_id)):view.delete_link(teacher_id, student_id)
                else:print('Link not exist')
            else:view.not_found('Teacher')
        else:view.not_found('Student')

    def generation_teacher(self):
        while 1:
            number = input("Enter count generation teacher:")
            if len(number) != 0 and number.isnumeric():
                start_time = time()
                database.gen_subject(int(int(number) / 30) + 1)
                database.gen_teachers(number)
                final_time = time() - start_time
                print("request execution time: ", final_time, "\n%s teachers successfully added" % number)
                break
            else:
                print("enter another teacher count")

    def generation_student(self):
        while 1:
            number = input("Enter count generation student:")
            if len(number) != 0 and number.isnumeric():
                start_time = time()
                database.gen_group(int(int(number) / 30) + 1)
                database.gen_students(number)
                final_time = time() - start_time
                print("request execution time: ", final_time, "\n%s student successfully added" % number)
                break
            else:
                print("enter another teacher count")

    def generation_links(self):
        start_time = time()
        database.gen_teacher_student_link()
        final_time = time() - start_time
        print("request execution time: ", final_time, "\nteacher-student links successfully added")