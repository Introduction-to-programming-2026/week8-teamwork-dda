import csv

# ── Step 1: Set up storage variables ─────────────────────────────────────────
scores = []          # we'll collect all scores here for the average
grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

# We track highest and lowest as dicts so we can store the name too
highest = {"name": "", "score": -1}
lowest  = {"name": "", "score": 101}   # Initialised to 101 so any real score is lower

# ── Step 2: Read the CSV ──────────────────────────────────────────────────────
# Note: Use "mini-projects/project2-grade-tracker/grades.csv" if running from root
with open("grades.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        name  = row["name"]
        # I converted the score from a string to an integer here because CSV data is read as text by default; this is necessary for the upcoming math calculations.
        score = int(row["score"])   # IMPORTANT: CSV values are strings — must convert

        # Append score to the scores list
        scores.append(score)

        # Update highest if this score is greater than highest["score"]
        # By using a dictionary for 'highest' and 'lowest', I can track both the numeric score and the student's name simultaneously as the loop iterates through the data.
        if score > highest["score"]:
            highest["score"] = score
            highest["name"] = name

        # Update lowest if this score is less than lowest["score"]
        if score < lowest["score"]:
            lowest["score"] = score
            lowest["name"] = name

        # Determine the letter grade using if/elif/else
        if score >= 90:
            letter = "A"
        elif score >= 80:
            letter = "B"
        elif score >= 70:
            letter = "C"
        elif score >= 60:
            letter = "D"
        else:
            letter = "F"
            
        # Increment grade_counts[letter] by 1
        grade_counts[letter] += 1

# ── Step 3: Calculate the average ────────────────────────────────────────────
# Calculate and round to 1 decimal place
# I used the sum() and len() functions to calculate the average and rounded it to one decimal place to keep the final output clean and readable.
average = round(sum(scores) / len(scores), 1) if scores else 0

# ── Step 4: Print the report ──────────────────────────────────────────────────
print("=== Quiz Grade Summary ===")
print(f"{'Students assessed':<18} : {len(scores)}")
print(f"{'Average score':<18} : {average}")
print(f"{'Highest score':<18} : {highest['score']}  ({highest['name']})")
print(f"{'Lowest score':<18} : {lowest['score']}  ({lowest['name']})")

print("\nGrade Distribution:")
# Accessing each letter grade from our dictionary
for grade in ["A", "B", "C", "D", "F"]:
    ranges = {"A": "90-100", "B": "80-89", "C": "70-79", "D": "60-69", "F": " 0-59"}
    print(f"  {grade} ({ranges[grade]}) : {grade_counts[grade]} students")
