from scipy.optimize import linear_sum_assignment
from src.matrix import DAAHSMatrixCreator

if __name__ == "__main__":
    matrix = DAAHSMatrixCreator().create_matrix()
    row_ind, col_ind = linear_sum_assignment(matrix.cost_matrix)
    print("tuff!")

    with open("data/current_matches.csv", "w") as file:
        print("tuff!")
        for i in range(len(row_ind)):
            print(i)
            row = row_ind[i]
            col = col_ind[i]
            # if matrix.cost_matrix[row][col] > 0:
            #     print("skipping")
            #     continue
            shared_subjects = [subject for subject in matrix.tutors[row].subjects if subject in matrix.tutees[col].subjects]
            file.write(f"{matrix.tutors[row].name},{matrix.tutees[col].name},{matrix.cost_matrix[row][col] + 500},{shared_subjects}\n")
