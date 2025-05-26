from match_scores import load_match_scores
from load_responses import load_responses

C = 500
PSEUDO_INF = 500**3

def create_matrix():
    tutors = []
    tutees = []

    responses = load_responses()

    match_scores = load_match_scores()
    match_score_dict = {(match.tutor, match.tutee): match.score for match in match_scores}

    for response in responses:
        if response.is_tutor():
            tutors.append(response)
        else:
            tutees.append(response)

    cost_matrix = [[0 for _ in range(len(tutees))] for _ in range(len(tutors))]

    for i in range(len(tutors)):
        tutor = tutors[i]

        for j in range(len(tutees)):
            tutee = tutees[j]

            common_subjects = [subject for subject in tutor.subjects if subject in tutee.subjects]

            if len(common_subjects) > 0:
                cost_matrix[i][j] = -C - match_score_dict.get((tutor.name, tutee.name), 0)
            else:
                cost_matrix[i][j] = PSEUDO_INF

    return (cost_matrix, tutors, tutees)

if __name__ == "__main__":
    print(create_matrix())
