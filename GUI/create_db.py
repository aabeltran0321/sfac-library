# import sqlite3

# # Connect to the SQLite database
# conn = sqlite3.connect('sfac_library.db')
# cursor = conn.cursor()

# # Update the genre
# cursor.execute("""
#     UPDATE Books
#     SET genre = 'General'
#     WHERE genre = 'Scientific';
# """)

# # Commit the changes and close the connection
# conn.commit()
# conn.close()

import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('sfac_library.db')
cursor = conn.cursor()

# Query to group RFID codes by genre
query = """
SELECT genre, GROUP_CONCAT(rfid_code, ', ') AS rfid_codes
FROM Books
GROUP BY genre;
"""

# Execute the query
cursor.execute(query)
results = cursor.fetchall()

# Transform the results into a dictionary
data = {genre: rfid_codes.split(', ') if rfid_codes else [] for genre, rfid_codes in results}

# Save the dictionary to a JSON file
output_file = 'rfid_codes_by_genre.json'
with open(output_file, 'w') as file:
    json.dump(data, file, indent=4)

# Close the connection
conn.close()

print(f"RFID codes grouped by genre have been saved to {output_file}")
