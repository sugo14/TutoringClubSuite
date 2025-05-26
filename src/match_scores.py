from load_responses import load_responses
import random

MATCH_SCORES_FILE = "sheets/match_scores.csv"

class MatchScore:
    def __init__(self, tutor, tutee, score):
        self.tutor = tutor
        self.tutee = tutee
        self.score = score

    def from_string(self, line):
        line = line.strip().split(",")
        self.tutor = line[0]
        self.tutee = line[1]
        self.score = int(line[2])
        return self

    def __repr__(self):
        return f"{self.tutor},{self.tutee},{self.score}"

def load_match_scores():
    with open("sheets/match_scores.csv", "r") as file:
        raw = file.readlines()
    l = [MatchScore(0, 0, 0).from_string(pairing) for pairing in raw]
    return l

def init_match_scores():
    tutor_subjects = {}
    tutee_subjects = {}

    responses = load_responses()

    for member in responses:
        for subject in member.subjects:
            if member.is_tutor():
                if subject not in tutor_subjects:
                    tutor_subjects[subject] = []
                tutor_subjects[subject].append(member.name)
            else:
                if subject not in tutee_subjects:
                    tutee_subjects[subject] = []
                tutee_subjects[subject].append(member.name)

    match_scores = []
    for subject in tutor_subjects:
        if subject not in tutee_subjects:
            continue
        for tutor in tutor_subjects[subject]:
            for tutee in tutee_subjects[subject]:
                if tutor != tutee:
                    # randomized for proof of concept
                    match_scores.append(MatchScore(tutor, tutee, random.randint(1, 10)))

    with open(MATCH_SCORES_FILE, "w") as file:
        for match_score in match_scores:
            file.write(match_score.__repr__() + "\n")
    
    return match_scores

if __name__ == "__main__":
    match_scores = init_match_scores()
    for match_score in match_scores:
        print(f"Tutor: {match_score.tutor}, Tutee: {match_score.tutee}, Score: {match_score.score}")
