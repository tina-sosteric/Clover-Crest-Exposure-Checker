import csv

# Convert the internal employee CSV into the plain "email:hash" format (for John the Ripper: no header row, no commas)

def export_hashes(csv_filepath, hash_filepath):
    with open(csv_filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        with open(hash_filepath, "w") as hash_file:
            for row in reader:
                email = row["email"]
                password_hash = row["password_hash"]
                hash_file.write(email + ":" + password_hash + "\n")

export_hashes("int_employees.csv", "internal_hashes.txt")