from math import log2
from abc import ABC, abstractmethod

from src.match_scores import load_match_scores
from src.responses import DAAHSMemberLoader, EduSparkMemberLoader, Member

C = 500
PSEUDO_INF = 500**3

class MatchCostMatrix:
    """
    This class contains a cost matrix for matches for tutors and tutees.
    Higher values indicate that the match is less desirable.
    """

    cost_matrix: list[list[int]]
    tutors: list[Member]
    tutees: list[Member]

    def __init__(self, cost_matrix: list[list[int]], tutors: list[Member], tutees: list[Member]):
        self.cost_matrix = cost_matrix
        self.tutors = tutors
        self.tutees = tutees

    def set_match_cost(self, tutor_index: int, tutee_index: int, cost: int):
        self.cost_matrix[tutor_index][tutee_index] = cost

    def get_match_cost(self, tutor_index: int, tutee_index: int) -> int:
        return self.cost_matrix[tutor_index][tutee_index]

class MatrixCreator(ABC):
    """
    This class is responsible for creating a MatchCostMatrix.
    It is provided a list of tutors and tutees, and may choose to access files.
    """

    @abstractmethod
    def create_matrix(self) -> MatchCostMatrix:
        pass

class DAAHSMatrixCreator(MatrixCreator):
    def create_matrix(self) -> MatchCostMatrix:
        """
        This loads the manually generated match scores from a file, and
        creates a cost matrix based on it.
        """

        # load tutor and tutee lists
        tutors = []
        tutees = []
        responses = DAAHSMemberLoader().load_members()
        for response in responses:
            if response.is_tutor():
                tutors.append(response)
            else:
                tutees.append(response)

        # load match scores into a nice dict
        # match_scores = load_match_scores()
        # match_score_dict = {(match.tutor, match.tutee): match.score for match in match_scores}

        # init cost matrix
        cost_matrix = [[0 for _ in range(len(tutees))] for _ in range(len(tutors))]

        # for each tutor-tutee pair, set cost
        # cost is infinite if they have no common subjects
        # otherwise, cost is a large negative constant minus the match score
        for i in range(len(tutors)):
            tutor = tutors[i]
            for j in range(len(tutees)):
                tutee = tutees[j]

                common_subjects = [subject for subject in tutor.subjects if subject in tutee.subjects]
                if len(common_subjects) > 0:
                    cost_matrix[i][j] = -C - len(common_subjects) + len(tutor.subjects)
                else:
                    cost_matrix[i][j] = PSEUDO_INF

        return MatchCostMatrix(cost_matrix, tutors, tutees)
    
class EduSparkMatrixCreator(MatrixCreator):
    def create_matrix(self) -> MatchCostMatrix:
        """
        This loads the manually generated match scores from a file, and
        creates a cost matrix based on it.
        """

        # load tutor and tutee lists
        tutors = []
        tutees = []
        responses = EduSparkMemberLoader().load_members()
        for response in responses:
            if response.is_tutor():
                tutors.append(response)
            else:
                tutees.append(response)

        # load match scores into a nice dict
        # match_scores = load_match_scores()
        # match_score_dict = {(match.tutor, match.tutee): match.score for match in match_scores}

        # init cost matrix
        cost_matrix = [[0 for _ in range(len(tutees))] for _ in range(len(tutors))]

        # for each tutor-tutee pair, set cost
        # cost is infinite if they have no common subjects
        # otherwise, cost is a large negative constant minus the match score
        for i in range(len(tutors)):
            tutor = tutors[i]
            for j in range(len(tutees)):
                tutee = tutees[j]

                # set score
                common_times = []
                # member.times is 9 lists, where index 0 is days available at 4:00 PM, index 1 is 4:30 PM, ..., index 8 is 8:00 PM
                # each sublist contains the days of the week the member is available at that time
                for k in range(9):
                    common_times.append([time for time in tutor.times[k] if time in tutee.times[k]])
                common_timeslots = 0
                days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                for day in days:
                    for k in range(1, len(common_times)): # times
                        if day in common_times[k - 1] and day in common_times[k]:
                            # the above checks that there are 2 30-min adjacent slots in a day
                            # forming a 1-hour slot
                            common_timeslots += 1
                common_subjects = [subject for subject in tutor.subjects if subject in tutee.subjects]
                common_grades = [grade for grade in tutor.grades if grade in tutee.grades]
                common_grade = len(common_grades) > 0

                # goal: maximize number of matches
                # then prioritize the tutor's grade choice
                # then maximize common availabilies and subjects
                if common_timeslots > 0:
                    cost_matrix[i][j] = 0 - C * 2 - 10 * common_grade - log2(len(common_subjects) + 4) - log2(common_timeslots + 4)
                else:
                    cost_matrix[i][j] = PSEUDO_INF

        return MatchCostMatrix(cost_matrix, tutors, tutees)

if __name__ == "__main__":
    print(DAAHSMatrixCreator().create_matrix())
