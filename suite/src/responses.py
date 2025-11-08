from abc import ABC, abstractmethod

RESPONSES_FILE = "sheets/2025sem1v2.tsv"
EDUSPARK_TUTOR_FILE = "sheets/eduspark-tutor.tsv"
EDUSPARK_STUDENT_FILE = "sheets/eduspark-student.tsv"

class Member:
    isTutor: bool
    subjects: list[str]
    name: str

    def __init__(self, isTutor, subjects, name):
        self.isTutor = isTutor  
        self.subjects = subjects
        self.name = name

    def is_tutor(self) -> bool:
        return self.isTutor
    
    def is_tutee(self) -> bool:
        return not self.isTutor
    
class EduSparkMember(Member):
    grades: list[str]
    times: list[list[str]]

    def __init__(self, isTutor, subjects, name, grades, times):
        new_subjects = []
        for subject in subjects:
            if subject == "English Language Arts":
                new_subjects.append("English")
            else:
                new_subjects.append(subject)
        super().__init__(isTutor, new_subjects, name)
        self.grades = grades
        self.times = times
    
class MemberLoader(ABC):
    @abstractmethod
    def load_members(self) -> list[Member]:
        pass

def getCourseFromHeaderElement(headerElement: str) -> str:
    if '[' in headerElement and ']' in headerElement:
        return headerElement.split('[')[1].split(']')[0]
    return headerElement

class DAAHSMemberLoader(MemberLoader):
    def load_members(self) -> list[Member]:
        header = []
        with open(RESPONSES_FILE, "r") as file:
            responses = file.readlines()
            header = responses[0].strip().split('\t')
            responses = responses[1:] # skip header
        members = []
        for response in responses:
            response = response.strip().split('\t') # tab separated
            print(response)
            # if len(response) != 3:
            #     print(f"Invalid response: {response}")
            #     continue
            name = response[1]
            isTutor = response[3] == "Tutor"
            subjects = []
            for i in range(len(header)):
                if len(header[i]) < 10 or header[i][0:9] != "Select th" or len(response) <= i:
                    continue
                streams = response[i].split(", ")
                course = getCourseFromHeaderElement(header[i])
                for stream in streams:
                    if stream == "":
                        continue
                    if subjects.count(course + stream) == 0:
                        subjects.append(course + stream)
                    if stream == "AP" and isTutor:
                        subjects.append(course + "-1 or Regular")
            members.append(Member(isTutor, subjects, name))
        return members
    
class EduSparkMemberLoader(MemberLoader):
    def load_members(self) -> list[EduSparkMember]:
        # tutors first
        header = []
        with open(EDUSPARK_TUTOR_FILE, "r") as file:
            responses = file.readlines()
            header = responses[0].strip().split('\t')
            responses = responses[1:] # skip header
        members = []
        for response in responses:
            response = response.split('\t') # tab separated
            print(response)
            # if len(response) != 3:
            #     print(f"Invalid response: {response}")
            #     continue
            name = response[2]
            grades_unedited = response[3].split(", ")
            grades = []
            if "Grade 1 - 3" in grades_unedited:
                grades.append("Grade 1")
                grades.append("Grade 2")
                grades.append("Grade 3")
            if "Grade 4 - 6" in grades_unedited:
                grades.append("Grade 4")
                grades.append("Grade 5")
                grades.append("Grade 6")
            if "Grade 7 - 9" in grades_unedited:
                grades.append("Grade 7")
                grades.append("Grade 8")
                grades.append("Grade 9")
            isTutor = True
            subjects = response[4].split(", ")
            if subjects == ['']:
                subjects = []
            times = []
            for i in range(len(header)):
                # print(i)
                # print(header[i])
                # print("---")
                # print(response[i])
                if not ("[" in header[i]):
                    continue
                days = response[i].split(", ")
                times.append(days)
            members.append(EduSparkMember(isTutor, subjects, name, grades, times))

        # now students
        header = []
        with open(EDUSPARK_STUDENT_FILE, "r") as file:
            responses = file.readlines()
            header = responses[0].strip().split('\t')
            responses = responses[1:] # skip header
        for response in responses:
            response = response.strip().split('\t') # tab separated
            print(response)
            # if len(response) != 3:
            #     print(f"Invalid response: {response}")
            #     continue
            name = response[3]
            grade = [response[7]]
            isTutor = False
            subjects = response[10].split(", ")
            if subjects == ['']:
                subjects = []
            times = []
            for i in range(len(header)):
                if not ("[" in header[i]):
                    continue
                days = response[i].split(", ")
                times.append(days)
            members.append(EduSparkMember(isTutor, subjects, name, grade, times))
        return members

if __name__ == "__main__":
    responses = EduSparkMemberLoader().load_members()
    for member in responses:
        print(f"Name: {member.name}, Is Tutor: {member.isTutor}, Subjects: {member.subjects}, Grades: {member.grades}, Times: {member.times}")
    print(f"Total members: {len(responses)}")
