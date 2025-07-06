from src.match_scores import load_match_scores, write_match_scores

spacer = "-" * 40
clear_screen = "\033[H\033[J"

if __name__ == "__main__":
    match_scores = load_match_scores()
    
    for match_score in match_scores:
        print(clear_screen + spacer + "\n")
        if match_score.score == -1:
            print(f"Tutor: {match_score.tutor}\n")
            print(f"Description: temp\n")
            print(f"Tutee: {match_score.tutee}\n")
            print(f"Description: temp\n")
            print(">>> Score: ", end = "")
            success = False
            while not success:
                try:
                    match_score.score = int(input())
                    print(f"\n{spacer}\n")
                    success = True
                except ValueError:
                    print("Invalid input. Please enter an integer score.")
                    success = False
                except (KeyboardInterrupt, EOFError):
                    print("\n\nExiting score assignment. Previous work was saved.\n")
                    exit(0)
        else:
            print(f"Pair {match_score.tutor} and {match_score.tutee} already scored.\n")
        write_match_scores(match_scores)
    print("All match scores have been assigned.")
