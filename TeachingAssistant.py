import Preference, Instructor, Course
class TeachingAssistant:
    def __init__(self, id, name, advisor, department):
        self.id = id
        self.name = name
        self.advisor = advisor
        self.department = department
        self.preferences = []

    def createPreference(self, id, course_id, ta_id, rank):
        p = Preference(id, None, course_id, rank)
        self.preferences.append(p)