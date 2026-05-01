import csv

# ── Step 1: Read the CSV and count languages ──────────────────────────────────
counts = {}

try:
    # Make sure the path matches your folder structure
   with open("part1/favorites.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Clean the data: remove whitespace and capitalize (e.g., "python" -> "Python")
            # I used .strip() and .capitalize() here so that 'python' and 'Python' aren't counted as different languages; this ensures our polling data stays accurate and clean.
            language = row["language"].strip().capitalize()

            # Update counts — increment if exists, create if new
            if language in counts:
                counts[language] += 1
            else:
                counts[language] = 1
except FileNotFoundError:
    print("Error: The file 'favorites.csv' was not found.")
    exit()

# ── Step 2: Sort by popularity (most popular first) ───────────────────────────
# I sorted the dictionary by values to show the most popular languages first, and added the percentage calculation to make the final report look more like a professional data analysis.
sorted_languages = sorted(counts, key=counts.get, reverse=True)
total_responses = sum(counts.values())

# ── Step 3: Print the report ──────────────────────────────────────────────────
print("=== Language Popularity Report ===")

# Using enumerate to get rank numbers (starting from 1)
for rank, language in enumerate(sorted_languages, start=1):
    count = counts[language]
    # Calculate percentage for a more professional look
    percentage = (count / total_responses) * 100
    
    # Formatting: language name aligned (10 chars), count, and percentage
    print(f"{rank}. {language:10} : {count:3} students ({percentage:.1f}%)")

# Print the total number of responses
print(f"\nTotal responses: {total_responses}")
