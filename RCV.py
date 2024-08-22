import csv
import random
import pandas as pd
import matplotlib.pyplot as plt


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
    writer.writerow(["Voter"] + [f"Choice {i+1}" for i in range(len(candidates))])

    for i in range(num_voters):
        # Generate unique candidate choices for each voter
        # vote = random.sample(candidates.tolist(), len(candidates))
        vote = random.sample(candidates, len(candidates))
        writer.writerow([f"Voter {i+1}"] + vote)

# Read the CSV file
df = pd.read_csv("votes.csv")


def RankedChoiceVotingRound(df, candidates, round_text):
    # Count the number of first-choice votes for each candidate
    first_choice_votes = df["Choice 1"].value_counts()

    total_votes = first_choice_votes.sum()
    # Print the results of the current round
    print(f"{round_text}")
    for candidate, votes in first_choice_votes.items():
        print(f"{candidate}: {votes} votes")
    print(f"Total Votes: {total_votes}\n")

    # Create a figure with two subplots
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Plot pie chart
    axs[0].pie(
        first_choice_votes,
        labels=[
            f"{candidate}\n({votes} votes)"
            for candidate, votes in first_choice_votes.items()
        ],
        autopct="%1.2f%%",
        startangle=140,
    )
    axs[0].set_title(f"{round_text} - Pie Chart")

    # Plot bar chart
    colors = plt.cm.tab20.colors[: len(first_choice_votes)]
    axs[1].bar(first_choice_votes.index, first_choice_votes.values, color=colors)
    axs[1].set_title(f"{round_text} - Bar Chart")
    axs[1].set_xlabel("Candidates")
    axs[1].set_ylabel("Number of Votes")
    axs[1].xaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Add whitespace between subplots
    fig.subplots_adjust(wspace=0.5)

    # Display the figure
    plt.show()

    # Identify the candidate with the fewest votes
    min_votes = first_choice_votes.min()
    eliminated_candidate = first_choice_votes[first_choice_votes == min_votes].index[0]
    print(f"Eliminated Candidate: {eliminated_candidate}\n")

    # Eliminate the candidate with the fewest votes
    candidates = [
        candidate for candidate in candidates if candidate != eliminated_candidate
    ]

    # Redistribute the votes of the eliminated candidate
    def redistribute_votes(row):
        if row["Choice 1"] == eliminated_candidate:
            for i in range(2, len(candidates) + 2):
                if row[f"Choice {i}"] in candidates:
                    return row[f"Choice {i}"]
            return None
        return row["Choice 1"]

    df["Choice 1"] = df.apply(redistribute_votes, axis=1)

    if len(candidates) == 1:
        return df, candidates, candidates[0]

    return df, candidates, None


# Initialize the list of winners
winners = []

# Create an array with a list of all the candidates
candidates = df["Choice 1"].unique()
eliminated_candidates = []

round_number = 1

while len(candidates) > 1:
    df, candidates, winner = RankedChoiceVotingRound(
        df, candidates, f"Round {round_number}"
    )

    round_number += 1

_, _, _ = RankedChoiceVotingRound(df, candidates, f"Round {round_number}")


# Print the winner
# winner = df['Choice 1'].value_counts().idxmax()
print(f"Winner: {winner}")
