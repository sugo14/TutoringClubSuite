from abc import ABC, abstractmethod

RESPONSES_FILE = "sheets/2025sem1v2.tsv"

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

if __name__ == "__main__":
    responses = DAAHSMemberLoader().load_members()
    for member in responses:
        print(f"Name: {member.name}, Is Tutor: {member.isTutor}, Subjects: {member.subjects}")
    print(f"Total members: {len(responses)}")
