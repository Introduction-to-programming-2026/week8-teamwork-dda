import csv

# ── Step 1: Set up storage variables ─────────────────────────────────────────
room_counts = {}
type_counts = {}
day_attendees = {}  # To find the busiest day
all_events = []     # To store every row for filtering and sorting

# ── Step 2: Read the CSV ──────────────────────────────────────────────────────
# Note: Ensure you are in the project3-event-log folder in your terminal
with open("bookings.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Extract columns
        date = row["date"]
        room = row["room"]
        event_type = row["event_type"]
        attendees = int(row["attendees"])

        # 1. Update room counts
        # I used the .get() method here to handle new keys safely; it prevents errors by providing a default value of 0 if the room or event type doesn't exist in the dictionary yet.
        room_counts[room] = room_counts.get(room, 0) + 1

        # 2. Update event type counts
        type_counts[event_type] = type_counts.get(event_type, 0) + 1

        # 3. Add attendees to the total for this date
        day_attendees[date] = day_attendees.get(date, 0) + attendees

        # 4. Save the row for later processing
        all_events.append(row)

# ── Step 3: Find the busiest day ──────────────────────────────────────────────
# Find the date (key) with the maximum attendance value
busiest_day = max(day_attendees, key=day_attendees.get)
busiest_count = day_attendees[busiest_day]

# ── Step 4: Filter large events (> 50 attendees) and sort ─────────────────────
# Using list comprehension to filter
# I implemented a list comprehension here to efficiently filter events with more than 50 attendees; it's a more Pythonic and concise way to create the filtered list in one line.
large_events = [row for row in all_events if int(row["attendees"]) > 50]

# Sort large_events by attendees descending (highest first)
# Using a lambda function as the sorting key allowed me to sort the data based on a specific column (attendees) in descending order, even though the data is stored in a complex list of dictionaries.
large_events_sorted = sorted(large_events, key=lambda row: int(row["attendees"]), reverse=True)

# ── Step 5: Print the report ──────────────────────────────────────────────────
print("=== Community Centre Booking Report ===\n")

print("Bookings by Room:")
for room in sorted(room_counts):
    print(f"  {room:8} : {room_counts[room]} events")

print("\nBookings by Event Type:")
for etype in sorted(type_counts):
    print(f"  {etype:9} : {type_counts[etype]} events")

print(f"\nBusiest Day: {busiest_day}  ({busiest_count} total attendees)")

print("\nLarge Events (> 50 attendees):")
for event in large_events_sorted:
    # Formatting for professional column alignment
    print(f"  {event['date']} | {event['room']:8} | {event['event_type']:9} |  {event['attendees']} attendees")
