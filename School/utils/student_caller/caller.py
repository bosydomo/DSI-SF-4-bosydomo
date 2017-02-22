import os
import numpy as np
from random import shuffle

class StudentCaller(object):

    dir_path            =   os.path.dirname(os.path.realpath(__file__))
    students            =   []
    absent_students     =   []
    active_students     =   []
    resource_defaults   =   {
        'questions':    'questions.txt',
        'students':     'students.txt '
    }

    def __init__(self, ask_questions=False, **options):

        super(StudentCaller, self).__init__()
        
        # Override class defaults if option and with existing class attribute
        for attribute, value in options.items():
            if hasattr(self, attribute):
                print "setting ", attribute
                setattr(self, attribute, value)

        self.ask_questions  =   ask_questions

        if self.ask_questions:
            self.load_resource(resource = "questions", shuffle = True)

    def set_resource(self, key, value):
        self.resource_defaults[key] = value

    def set_students(self, students):
        """
        Dynamically override an instance of students variables.
        """
        self.students = students

    def set_absent_students(self, absent_students=[]):
        """
        Will remove matching students from student list
        """
        self.students = list(set(self.students) - set(absent_students))

    def load_resource(self, resource='questions', randomize=True):
        """
        Dynamically load class meta-resources and set to class attributes.
        Params: resource str: resource key, shuffle bool: shuffle order of resource items
        """
        with open(self.dir_path + "/" + self.resource_defaults[resource], 'r') as f:
            lines = f.readlines()

        lines = [x.rstrip() for x in lines if not len(x) == 0]
      
        if randomize:
            shuffle(lines)
 
        setattr(self, resource, lines)

    def load_questions(self):
        pass

    def ask_question(self):
        print self.questions.pop()

    def get_student(self):
        if len(self.active_students) == 0:
            students = np.repeat(self.students, 2)
            self.active_students = np.random.choice(students,
                                             size=len(students),
                                             replace=False).tolist()
        return self.active_students.pop()

    def __call__(self):
        print self.get_student()

        if self.ask_questions:
            self.ask_question()

