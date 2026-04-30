import csv
import sqlite3

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — CREATE THE DATABASE AND TABLE (Coder A)
# ══════════════════════════════════════════════════════════════════════════════

conn = sqlite3.connect("survey.db")
db   = conn.cursor()

# Create the responses table with appropriate data types
db.execute('''CREATE TABLE IF NOT EXISTS responses (
    student_id TEXT,
    faculty TEXT,
    year INTEGER,
    satisfaction INTEGER,
    favourite_tool TEXT,
    comments TEXT
)''')


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — READ ALL THREE CSV FILES AND INSERT ROWS (Coder A)
# ══════════════════════════════════════════════════════════════════════════════

csv_files = [
    "faculty_science.csv",
    "faculty_arts.csv",
    "faculty_business.csv",
]

for filename in csv_files:
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # MANDATORY: Use ? placeholders to prevent SQL injection
                db.execute("INSERT INTO responses VALUES (?, ?, ?, ?, ?, ?)", 
                           (row['student_id'], row['faculty'], int(row['year']), 
                            int(row['satisfaction']), row['favourite_tool'], row['comments']))
    except FileNotFoundError:
        print(f"Warning: {filename} not found.")

conn.commit()
print("Database loaded successfully.\n")


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — DASHBOARD QUERIES
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 30)
print("  UNIVERSITY SURVEY DASHBOARD")
print("=" * 30)

# ── Query 1: Total responses by faculty (Coder B) ────────────────────────────
print("\n1. Total Responses by Faculty")

rows = db.execute("SELECT faculty, COUNT(*) AS n FROM responses GROUP BY faculty ORDER BY faculty").fetchall()
total = 0
for row in rows:
    faculty, count = row
    print(f"   {faculty:<10}: {count}")
    total += count
print(f"   {'TOTAL':<10}: {total}")


# ── Query 2: Average satisfaction by year (Coder B) ──────────────────────────
print("\n2. Average Satisfaction by Year of Study")

rows = db.execute("SELECT year, ROUND(AVG(satisfaction), 1) AS avg_sat FROM responses GROUP BY year ORDER BY year").fetchall()
for row in rows:
    year, avg_sat = row
    print(f"   Year {year} : {avg_sat} / 5")


# ── Query 3: Favourite tool popularity (Coder B) ─────────────────────────────
print("\n3. Favourite Tool Popularity")

rows = db.execute("SELECT favourite_tool, COUNT(*) AS n FROM responses GROUP BY favourite_tool ORDER BY n DESC").fetchall()
for row in rows:
    tool, count = row
    print(f"   {tool:<10}: {count:>2} students")


# ── Query 4: Faculty comparison table (Coder C) ──────────────────────────────
print("\n4. Faculty Comparison")
print(f"   {'Faculty':<12} | {'Avg Satisfaction':<18} | Most Popular Tool")
print("   " + "-" * 50)

faculties = ["Arts", "Business", "Science"]
for faculty in faculties:
    # Query average satisfaction for this faculty
    avg_row = db.execute(
        "SELECT ROUND(AVG(satisfaction), 1) AS avg FROM responses WHERE faculty = ?",
        (faculty,)
    ).fetchone()

    # Query the most popular tool for this faculty
    tool_row = db.execute(
        "SELECT favourite_tool FROM responses WHERE faculty = ? GROUP BY favourite_tool ORDER BY COUNT(*) DESC LIMIT 1",
        (faculty,)
    ).fetchone()

    avg_val = avg_row[0] if avg_row else 0.0
    tool_val = tool_row[0] if tool_row else "N/A"
    
    print(f"   {faculty:<12} | {avg_val:<18} | {tool_val}")


# ── Query 5: Interactive filter (Coder C) ────────────────────────────────────
print()
try:
    user_input = input("Enter minimum satisfaction score (1-5): ")
    min_score = int(user_input)
except ValueError:
    print("Invalid input. Defaulting to 4.")
    min_score = 4

# Use ? placeholder for user-provided min_score
rows = db.execute("""
    SELECT student_id, faculty, year, favourite_tool 
    FROM responses 
    WHERE satisfaction >= ? 
    ORDER BY faculty, year
""", (min_score,)).fetchall()

print(f"\nStudents with satisfaction >= {min_score}:")
if not rows:
    print("  No results found.")
for row in rows:
    sid, fac, yr, tool = row
    print(f"   {sid} | {fac:<10} | Year {yr} | {tool}")


# ══════════════════════════════════════════════════════════════════════════════
# CLEANUP
# ══════════════════════════════════════════════════════════════════════════════
conn.close()