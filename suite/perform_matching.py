from scipy.optimize import linear_sum_assignment
from src.matrix import create_matrix

if __name__ == "__main__":
    cost_matrix, tutors, tutees = create_matrix()

    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    with open("sheets/current_matches.csv", "w") as file:
        for row, col in zip(row_ind, col_ind):
            if cost_matrix[row][col] > 0:
                continue
            file.write(f"{tutors[row].name},{tutees[col].name},{-cost_matrix[row][col] - 500}\n")
