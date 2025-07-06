from src.match_scores import init_match_scores

if __name__ == "__main__":
    print("Are you sure you want to reset ALL match scores? This will completely overwrite all previous match score work.")
    confirmation = input("\nType 'I accept' to confirm:\n\n>>> ")
    print("")
    if confirmation == "I accept":
        print("Resetting match scores...")
        match_scores = init_match_scores()
    else:
        print("Reset cancelled.")
