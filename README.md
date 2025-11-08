# Tutoring Club Suite

A collection of useful CLI programs that automate parts of running a tutoring club. Currently includes optimal tutor-tutee matching, as well as other supporting scripts.

This is currently very much a work in progress, although I am working towards modularity.

# How Matching Works

Matching has two basic parts:

- Generating the cost matrix for all pairs of tutors and tutees
- Performing the matches using the Hungarian Algorithm

The cost matrix can be constructed to optimize for any heuristic, such as maximizing number of matches.
