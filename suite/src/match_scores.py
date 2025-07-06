from src.responses import load_responses
import random

MATCH_SCORES_FILE = "data/match_scores.csv"

class MatchScore:
    @staticmethod
    def default() -> "MatchScore":
        return MatchScore("", "", -1)

    def __init__(self, tutor: str, tutee: str, score: int):
        self.tutor = tutor
        self.tutee = tutee
        self.score = score

    def from_string(line: str) -> "MatchScore":
        line = line.strip().split(",")
        match_score = MatchScore.default()
        match_score.tutor = line[0]
        match_score.tutee = line[1]
        match_score.score = int(line[2])
        return match_score

    def __repr__(self) -> str:
        return f"{self.tutor},{self.tutee},{self.score}"

def init_match_scores() -> list[MatchScore]:
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
                    match_scores.append(MatchScore(tutor, tutee, -1))

    with open(MATCH_SCORES_FILE, "w") as file:
        for match_score in match_scores:
            file.write(match_score.__repr__() + "\n")
    
    return match_scores

def load_match_scores() -> list[MatchScore]:
    with open(MATCH_SCORES_FILE, "r") as file:
        raw = file.readlines()
    # raw = [line.strip() for line in raw if line.strip()]
    l = [MatchScore.from_string(pairing) for pairing in raw]
    return l

def write_match_scores(match_scores: list[MatchScore]) -> None:
    with open(MATCH_SCORES_FILE, "w") as file:
        for match_score in match_scores:
            file.write(match_score.__repr__() + "\n")
