import Preference
import Instructor as i
import Course as c
import TeachingAssistant as t
from random import shuffle
import random

class Assignment:
    def __init__(self, preference_list, ta_list, course_list, instructor_list):
        self.preference_list = preference_list
        self.ta_list = ta_list
        self.course_list = course_list
        self.instructor_list = instructor_list

    def check_preferences(self):
        from random import randint

        for instructor in self.instructor_list:
            for course in instructor.courses:
                #get the number of preferences for each specific course

                course_preferences = []
                final_list = []
                final_ids = []
                available_ranks = []

                for pref in instructor.preferences:
                    if pref.course_id == course.id:
                        course_preferences.append(pref)
                        # to remove the duplicate preferences
                        if pref.ta_id not in final_ids:
                            final_list.append(pref)
                            final_ids.append(pref.ta_id)
                            available_ranks.append(pref.rank)
                        else:
                            index = instructor.preferences.index(pref)
                            instructor.preferences.pop(index)

                course_preferences = final_list
                preference_per_course = len(course_preferences)

                if preference_per_course == 10:
                    continue
                else:
                    nr_of_preferences = preference_per_course

                    if nr_of_preferences > 10:
                        #if there are more than 10 preferences
                        index = nr_of_preferences
                        while index != nr_of_preferences:
                            instructor.preferences.pop(index-1)
                            index = index - 1
                    else:
                        #if there are less than 10 preferences
                        required_pref = 10 - nr_of_preferences

                        not_available_ranks = []
                        count = 1
                        while count < 11:
                            if count not in available_ranks:
                                not_available_ranks.append(count)
                            count = count + 1
                        not_available_ranks.reverse()

                        while required_pref != 0:

                            random_number = randint(0, len(self.ta_list)-1)
                            valid_preference = True

                            for pref in instructor.preferences:
                                if pref.ta_id == self.ta_list[random_number].id and course.id == pref.course_id:
                                    #if this ta is already in preference list
                                    valid_preference = False
                                    break

                            if valid_preference:
                                instructor.createPreference(instructor.id,self.ta_list[random_number].id, course.id, not_available_ranks.pop())
                                nr_of_preferences = nr_of_preferences + 1
                                required_pref = required_pref - 1


        for ta in self.ta_list:

            ta_preferences = ta.preferences

            final_list = []
            final_ids = []
            available_ranks = []

            # to remove the duplicate preferences
            for pref in ta.preferences:
                if pref.course_id not in final_ids:
                    final_list.append(pref)
                    final_ids.append(pref.course_id)
                    available_ranks.append(pref.rank)
                else:
                    index = ta.preferences.index(pref)
                    ta.preferences.pop(index)

            ta_preferences = final_list

            if len(ta_preferences) == 10:
                continue
            else:
                nr_of_preferences = len(ta_preferences)

                not_available_ranks = []
                count = 1
                while count < 11:
                    if count not in available_ranks:
                        not_available_ranks.append(count)
                    count = count + 1
                not_available_ranks.reverse()

                if nr_of_preferences > 10:
                    #if there are more than 10 preferences
                    index = nr_of_preferences
                    while index != nr_of_preferences:
                        ta_preferences.pop(index-1)
                        index = index - 1
                else:
                    #if there are less than 10 preferences
                    required_pref = 10 - nr_of_preferences

                    while required_pref != 0:

                        random_number = randint(0, len(self.course_list)-1)
                        valid_preference = True

                        for pref in ta.preferences:
                            if pref.course_id == self.course_list[random_number].id:
                                #if this ta is already in preference list
                                valid_preference = False
                                break

                        if valid_preference:
                            ta.createPreference(ta.id, self.course_list[random_number].id, None, not_available_ranks.pop())
                            required_pref = required_pref - 1


    def check_constraints(self):
        print('no code yet')

    def assign_random_preference(self):
        print('no code yet')

    def score(self, chromosome, courselist,instructorlist, numberOfPref, empFactor, wi, wta):

        index = 0
        courseSatisfaction=[]

        for c in range(len(courselist)):
            assignedTAs = []

            instructor=None
            for i in range(len(instructorlist)):
                if instructorlist[i].id==courselist[c].instructor:
                    instructor=instructorlist[i]

            taneed = int(courselist[c].ta_need)
            instructor_satisfaction=0
            overall_ta_satisfaction=0

            for t in range(taneed):
                assignedTAs.append(chromosome[index])
                index += index

            # instructor satisfaction for c

            for x in range(len(assignedTAs)):
                for p in range(len(instructor.preferences)):

                    if instructor.preferences[p].ta_id == assignedTAs[x].id:
                        instructor_satisfaction+= (numberOfPref+1-instructor.preferences[p].rank)^empFactor

            base_case=0

            for x in range(len(assignedTAs)):
                base_case+= (numberOfPref-x)^empFactor

            instructor_satisfaction=(instructor_satisfaction/base_case)*100

            # ta satisfaction for c

            for k in range(len(assignedTAs)):
                for p in range(len(assignedTAs[k].preferences)):

                    if assignedTAs[k].preferences[p].course_id== courselist[c].id:
                        overall_ta_satisfaction += (((numberOfPref+1-assignedTAs[k].preferences[p].rank)^empFactor) / (numberOfPref^empFactor))*100

            overall_ta_satisfaction= overall_ta_satisfaction/taneed

            # satisfaction for c

            satisfaction=(wi*instructor_satisfaction + wta*overall_ta_satisfaction)/(wi+wta)
            courseSatisfaction.append(satisfaction)

        #tot = 0
        #for cs in range(len(courseSatisfaction)):
        #    tot += courseSatisfaction[cs]
        #return tot / (len(courseSatisfaction))
        return courseSatisfaction

    def assign(self):
        print('no code yet')

    def initialize(self,populationSize,totalTANeed,taList,population):

        for n in range(populationSize):
            chromosome = []

            for j in range(totalTANeed):
                if j < len(taList):
                    chromosome.append(taList[j])
                else:
                    chromosome.append(None)

            shuffle(chromosome)

            population[n][:] = chromosome

        return population

    def crossover(self,chromosome1,chromosome2):

        cp=random.randint(0,len(chromosome1)-1)
        tempTa=chromosome1[cp]
        chromosome1[cp]=chromosome2[cp]
        chromosome2[cp]=tempTa

        return chromosome1,chromosome2

    def mutation(self,chromosome1):

        mp1 =random.randint(0,len(chromosome1)-1)
        mp2 =random.randint(0,len(chromosome1)-1)

        while mp2 == mp1:
            mp2 = random.randint(0,len(chromosome1)-1)

        tempTa=chromosome1[mp1]
        chromosome1[mp1]=chromosome1[mp2]
        chromosome1[mp2]= tempTa

        return chromosome1


def main():
    print('Welcome to Senior Design Project.')
    course_list = []
    instructor_list = []
    ta_list = []
    preference_list = []
    ta_course_list = []

    populationSize = 50
    totalTANeed = 0
    numberOfPref=10
    empFactor=3
    wi=2
    wta=1
    #ca advisor constant

    with open("courses.txt", "r") as ins:
        array = []
        count = 0
        for line in ins:
            if count > 0:
                #print(line)
                index = line.index("\t")
                index2 = line.index("\t", index+1)
                code = line[0: index]
                ta_need =line[index+1 : index2]
                instructor = line[index2 + 1: len(line)].strip()
                array.append(line)
                course = c.Course(code, ' ', ' ', instructor, ta_need)
                course_list.append(course)
                ta_course_list.append((instructor, code))
            count = count + 1


    with open("pref.txt", "r") as ins:
        array = []
        count = 0
        for line in ins:
            if count > 0:
                array.append(line)
                index = line.index("\t")
                code = line[0: index]
                index2 = line.index("\t", index+1)
                course = line[index+1: index2]
                prefs =line[index2+1 : len(line)].strip()
                instructor = i.Instructor(code, ' ', [], [], ' ')
                instructor_list.append(instructor)
                rank = 1
                prev_index = -1
                index3 = 0
                while index3 < len(prefs):
                    try:
                        index3 = prefs.index("\t", index3+1)
                        if len(prefs[prev_index+1:index3]) > 1:
                            instructor.createPreference(code, prefs[prev_index+1:index3], course, rank)
                            rank = rank + 1
                            prev_index = index3
                    except:
                        if len(prefs[prev_index + 1:index3]) > 1:
                            instructor.createPreference(code, prefs[prev_index+1:len(prefs)], course, rank)
                        break
            count = count + 1

        #print(instructor_list)
        for instructor in instructor_list:
            for tuple in ta_course_list:
                if instructor.id in tuple:
                    for course in course_list:
                        if course.id == tuple[1]:
                            instructor.courses.append(course)



    with open("talist.txt", "r") as ins:
        array = []
        count = 0
        advisor_advisee = []
        for line in ins:
            if count > 0:
                #line.strip().replace("\t", ' ')
                index = line.index("\t")
                tanumber = line[0: index]
                advisor =line[index+1 : len(line)]
                array.append(line)
                ta = t.TeachingAssistant(tanumber, ' ', advisor, ' ')
                ta_list.append(ta)
                advisor_advisee.append((ta, advisor))
            count = count + 1

        for instructor in instructor_list:
            for tuple in advisor_advisee:
                if instructor.id in tuple:
                    instructor.students.append(tuple[0])


    with open("tapref.txt", "r") as ins:
        array = []
        count = 0
        for line in ins:
            if count > 0:
                # line.strip().replace("\t", ' ')
                index = line.index("\t")
                code = line[0: index]
                prefs = line[index + 1: len(line)]
                array.append(line)
                rank = 1
                prev_index = -1
                index3 = 0

                current_ta = None
                for ta in ta_list:
                    if ta.id == code:
                        while index3 < len(prefs):
                            try:
                                index3 = prefs.index("\t", index3+1)
                                if len(prefs[prev_index + 1:index3]) > 1:
                                    ta.createPreference(code, prefs[prev_index+1:index3], None, rank)
                                    rank = rank + 1
                                prev_index = index3
                            except:
                                if len(prefs[prev_index + 1:index3]) > 1:
                                    ta.createPreference(code, prefs[prev_index+1:len(prefs)], None, rank)
                                break
                        break


            count = count + 1


    a = Assignment(preference_list, ta_list, course_list, instructor_list)
    #
    # print('Before checking: ')
    # for ins in instructor_list:
    #     print(ins.id)
    #     print('--')
    #     for pref in ins.preferences:
    #         print pref.course_id, pref.ta_id, pref.rank
    #     #
    # for ta in ta_list:
    #     print(ta.id)
    #     print('--')
    #     for pref in ta.preferences:
    #         print pref.course_id, pref.ta_id, pref.rank

    a.check_preferences()
    # print('After checking: ')

    # for ins in a.instructor_list:
    #     print(ins.id)
    #     print('--')
    #     for pref in ins.preferences:
    #         print pref.course_id, pref.ta_id, pref.rank


    # for ta in a.ta_list:
    #     print(ta.id)
    #     print('--')
    #     for pref in ta.preferences:
    #         print pref.course_id, pref.ta_id, pref.rank

    for z in range(len(course_list)):
        totalTANeed += int(course_list[z].ta_need)

    population = [[0 for m in xrange(totalTANeed)] for n in xrange(populationSize)]

    a.initialize(populationSize,totalTANeed ,ta_list,population)

    g1=population[1]
    g2=population[2]
    s1=a.score(g1, course_list, instructor_list,numberOfPref, empFactor, wi, wta)
    s2=a.score(g2, course_list, instructor_list,numberOfPref, empFactor, wi, wta)

    print s1

    for j in range(10):
        g1,g2=a.crossover(g1,g2)
        mut_prob = random.randint(0, 100)
        if mut_prob > 50:
            a.mutation(g1)
        print a.score(g1, course_list, instructor_list,numberOfPref, empFactor, wi, wta)

if __name__ == '__main__':
	main()





