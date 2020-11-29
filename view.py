class View:
    def print_items(self,items):
        if(items):
            print("-----------------------------------------------------------------------------------------")
            for item in items:
                print(item)
            print("-----------------------------------------------------------------------------------------")

    def print_string(self,string):
        print("-----------------------------------------------------------------------------------------")
        print(string)
        print("-----------------------------------------------------------------------------------------")

    def not_found(self, item): self.print_string('%s not found' % (item))

    #Teacher and Student command
    def create_item(self,item,item_id):self.print_string('%s successfully added with id -> %s'% (item,item_id))

    def delete_item(self, item, item_id): self.print_string('%s with id -> %s successfully deleted' % (item, item_id))

    def update_item(self,item,item_id):self.print_string('%s with id -> %s successfully updated' % (item, item_id))

    #Email and Phone command
    def create_phone(self, item_id): self.print_string('Student phone successfully added with phone number (%s)' % (item_id))

    def create_email(self, item_id): self.print_string('Teacher email successfully added email address (%s)' % (item_id))

    def delete_phone_email(self, item, item_id): self.print_string('%s (%s) successfully deleted' % (item, item_id))

    #Link command
    def create_link(self,teacher_id,student_id):self.print_string('Teacher <-> Student link successfully added'
                                                        ' with teacher id -> %s and student id -> %s'% (teacher_id,student_id))

    def delete_link(self,teacher_id,student_id):self.print_string('Teacher <-> Student link with teacher id -> %s'
                                                        ' and student id -> %s successfully deleted '% (teacher_id,student_id))

