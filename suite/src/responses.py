RESPONSES_FILE = "sheets/responses.tsv"

class Member:
    def __init__(self, response):
        # remove ending newline
        response = response[:-1].split('\t') # tab
        if len(response) != 4:
            print(f"Invalid response: {response}")
            return None
        self.timestamp = response[0]
        self.isTutor = response[1] == "Tutor"
        self.subjects = response[2].split(", ")
        self.name = response[3]

    def is_tutor(self) -> bool:
        return self.isTutor
    
    def is_tutee(self) -> bool:
        return not self.isTutor

def load_responses() -> list[Member]:
    with open(RESPONSES_FILE, "r") as file:
        responses = file.readlines()[1:] # skip header
    members = [Member(response) for response in responses]
    return members

if __name__ == "__main__":
    responses = load_responses()
    for member in responses:
        print(f"Name: {member.name}, Is Tutor: {member.isTutor}, Subjects: {member.subjects}")
    print(f"Total members: {len(responses)}")
