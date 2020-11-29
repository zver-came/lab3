class Search:

    def __init__(self):
        self.main_tables={}
        self.column = {}
        self.likes={}

    def teacher_params(self):
        self.main_tables['teachers as t'] = None
        while 1:
            print("----------------------------------------------------------------------")
            print("Teacher params\n-> name\n-> surname\n-> id\n-> email\n-> subject\n-> skip")
            input_line= input("Enter params:").strip()
            if input_line== "name":
                input_line = input("Enter name: ").strip()
                if (len(input_line) != 0):
                    self.main_tables['teachers as t'] = "teachers"
                    self.likes['t.name'] = input_line
                    self.column['t.teacher_id,t.name,t.surname'] = "teachers"
            elif input_line== "surname":
                input_line = input("Enter surname: ").strip()
                if (len(input_line) != 0):
                    self.main_tables['teachers as t'] = "teachers"
                    self.likes['t.surname'] = input_line
                    self.column['t.teacher_id,t.name,t.surname'] = "teachers"
            elif input_line == "id":
                input_line = input("Enter teacher id: ").strip()
                if (len(input_line) != 0):
                    try:
                        input_line =int(input_line)
                        self.likes['cast(t.teacher_id as varchar(20))'] = str(input_line)
                        self.main_tables['teachers as t'] = "teachers"
                        self.column['t.teacher_id,t.name,t.surname'] = "teachers"
                    except:print("Don`t enter student id -> ",input_line)
            elif input_line== "email":
                input_line = input("Enter email: ").strip()
                if (len(input_line) != 0):
                    self.main_tables['teachers as t'] = "teachers"
                    self.column['t.teacher_id,t.name,t.surname'] = "teachers"
                    self.likes['te.email'] = input_line
                    self.main_tables[' join teacher_email as te using(teacher_id) '] = "teacher_email"
                    self.column['te.email']="email"
            elif input_line == "subject":
                input_line = input("Enter subject: ").strip()
                if (len(input_line) != 0):
                    self.main_tables[' join subjects as sub using(subject_id) '] = "subjects"
                    self.column['sub.subject_id,sub.name'] = "subjects"
                    self.likes['sub.name'] = input_line
            elif input_line== "skip":
                if(self.main_tables['teachers as t']!=None):
                    break
            else:print("Enter enather command")

    def student_params(self):
        self.main_tables['students as s'] = None
        while 1:
            print("Student params:\n-> name\n-> surname\n-> id\n-> phone\n-> group\n-> skip")
            input_line= input("Enter params:").strip()
            if input_line== "name":
                input_line= input("Enter name: ").strip()
                if (len(input_line)!=0):
                    self.main_tables['students as s'] = "students"
                    self.column['s.student_id,s.name,s.surname']="students"
                    self.likes['s.name']=input_line
            elif input_line== "surname":
                input_line = input("Enter surname: ").strip()
                if (len(input_line) != 0):
                    self.main_tables['students as s'] = "students"
                    self.column['s.student_id,s.name,s.surname'] = "students"
                    self.likes['s.surname']=input_line
            elif input_line == "id":
                input_line = input("Enter student id: ").strip()
                if (len(input_line) != 0):
                    try:
                        input_line =int(input_line)
                        self.likes['cast(s.student_id as varchar(20))'] = str(input_line)
                        self.main_tables['students as s'] = "students"
                        self.column['s.student_id,s.name,s.surname'] = "students"
                    except:print("Don`t enter student id -> ",input_line)
            elif input_line== "phone":
                input_line = input("Enter phone: ").strip()
                if (len(input_line) != 0):
                    try:
                        input_line =int(input_line)
                        self.main_tables['students as s'] = "students"
                        self.column['s.student_id,s.name,s.surname'] = "students"
                        self.column['sp.phone_number'] = "students phone"
                        self.main_tables[' join student_phone as sp using(student_id) '] = "student_phone"
                        self.likes['cast(sp.phone_number as varchar(20))'] = str(input_line)
                    except:print("Don`t enter student phone -> ",input_line)
            elif input_line == "group":
                input_line = input("Enter group: ").strip()
                if (len(input_line) != 0):
                    if (len(input_line) != 0):
                        self.main_tables[' join groups as g using(group_id) '] = "groups"
                        self.column['g.group_id,g.name'] = "groups"
                        self.likes['cast(g.name as varchar(20))'] = input_line
            elif input_line== "skip":
                if (self.main_tables['students as s'] != None):
                    break
            else:print("Enter enather command")

    def find_group(self):
        self.main_tables[' groups as g '] = None
        while 1:
            print("----------------------------------------------------------------------")
            print("Group params\n-> name\n-> id\n-> skip")
            input_line = input("Enter params:").strip()
            if input_line == "name":
                input_line = input("Enter group name: ").strip()
                if (len(input_line) != 0):
                    self.main_tables[' groups as g '] = "groups"
                    self.column['g.group_id,g.name'] = "groups"
                    self.likes['g.name'] = input_line
            elif input_line == "skip":
                if (self.main_tables[' groups as g '] != None):
                    break
            elif input_line == "id":
                input_line = input("Enter subject id: ").strip()
                if (len(input_line) != 0):
                    try:
                        input_line=int(input_line)
                        self.main_tables[' groups as g '] = "grounps"
                        self.column[' g.group_id,g.name'] = "grounps"
                        self.likes['cast(g.group_id as varchar(20))'] = str(input_line)
                    except:print("Don`t enter this id")
            else:print("Enter anather command")

    def find_subject(self):
        self.main_tables[' subjects as sub '] = None
        while 1:
            print("----------------------------------------------------------------------")
            print("Subject params\n-> name\n-> id\n-> skip")
            input_line = input("Enter params:").strip()
            if input_line == "name":
                input_line = input("Enter subject name: ").strip()
                if (len(input_line) != 0):
                    self.main_tables[' subjects as sub '] = "subjects"
                    self.column['sub.subject_id,sub.name'] = "subjects"
                    self.likes['sub.name'] = input_line
            elif input_line == "skip":
                if (self.main_tables[' subjects as sub '] != None):
                    break
            elif input_line == "id":
                input_line = input("Enter subject id: ").strip()
                if (len(input_line) != 0):
                    try:
                        input_line=int(input_line)
                        self.main_tables[' subjects as sub '] = "subjects"
                        self.column['sub.subject_id,sub.name'] = "subjects"
                        self.likes['cast(sub.subject_id as varchar(20))'] = str(input_line)
                    except:print("Don`t enter this id")
            else:print("Enter anather command")

    def create_query(self):
        query="select "
        for column in self.column:
            query+=column+","
        query=query[0:len(query)-1]
        query+=" from "
        for main_table in self.main_tables:
            query+=main_table
        query+=" where "
        for where in self.likes:
            query+=where+" like \'%"
            query+=self.likes[where]+"%\' and "
        query = query[0:len(query) - 5]
        self.likes={}
        self.column={}
        self.main_tables={}
        return (query)