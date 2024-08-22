import csv
import random

# Define the candidates
candidates = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank"]
eliminated_candidates = []

# Create vote data (each sublist represents a voter's ranked choices)
votes = []
num_voters = 1000

# for _ in range(num_voters):
#     vote = random.sample(candidates, len(candidates))
#     votes.append(vote)

# Write the data to a CSV file
with open("votes.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["voter"] + [f"choice_{i+1}" for i in range(len(candidates))])

    for i in range(num_voters):
        # Generate unique candidate choices for each voter
        # vote = random.sample(candidates.tolist(), len(candidates))
        vote = random.sample(candidates, len(candidates))
        writer.writerow([f"voter {i+1}"] + vote)
