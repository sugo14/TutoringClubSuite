from scipy.optimize import linear_sum_assignment
from src.matrix import DAAHSMatrixCreator, EduSparkMatrixCreator

if __name__ == "__main__":
    matrix = EduSparkMatrixCreator().create_matrix()
    row_ind, col_ind = linear_sum_assignment(matrix.cost_matrix)
    print("tuff!")

    with open("data/current_matches.tsv", "w") as file:
        print("tuff!")
        for i in range(len(row_ind)):
            print(i)
            row = row_ind[i]
            col = col_ind[i]
            # if matrix.cost_matrix[row][col] > 0:
            #     print("skipping")
            #     continue
            shared_subjects = [subject for subject in matrix.tutors[row].subjects if subject in matrix.tutees[col].subjects]
            common_times = []
            for j in range(9):
                common_times.append([time for time in matrix.tutors[row].times[j] if time in matrix.tutees[col].times[j]])
            common_timeslots = []
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            for day in days:
                for j in range(1, len(common_times)): # days
                    if day in common_times[j - 1] and day in common_times[j]:
                        # times start at 4:00 PM (common_times[0]), to 8:00 PM (common_times[4]) in 30 min increments
                        time = 4 + 0.5 * (j - 1)
                        str_time = f"{int(time)}:00" if time.is_integer() else f"{int(time)}:30"
                        common_timeslots.append(day + " at " + str_time + " PM")

            match_successful = matrix.cost_matrix[row][col] < 0
            file.write(f"{matrix.tutors[row].name}\t{matrix.tutees[col].name}\t{"Success" if match_successful else "Failed"}\t{", ".join(common_timeslots)}\t{', '.join(shared_subjects)}\n")

    print("done")
