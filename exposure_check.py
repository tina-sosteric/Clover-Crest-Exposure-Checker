# Import the tools for this file.

import hashlib
import csv
from collections import Counter

# Read the internal employee list back into a dictionary (email & password hash).

def load_int_users(filepath):
    users = {}
    with open(filepath, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            email = row["email"]
            password_hash = row["password_hash"]
            users[email] = password_hash
    return users

# Read the leaked dump into a dictionary (email & plaintext password).

def load_ext_dump(filepath):
    dump = {}
    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()
            email, password = line.split(",")
            email = email.strip()
            password = password.strip()
            dump[email] = password

    return dump

# Find potential employee matches from the dump.

def find_matches(dump, int_users):
    matches = []
    for email, password in dump.items():
        if email in int_users:
            matches.append((email, password))
    return matches

 # Hash leaked password & compare hashes.

def score_match(email, leaked_password, int_users):
    """
    Code below decides which employees need prioritization (the worst cases before everyone else).
    """
    leaked_hash = hashlib.sha256(leaked_password.encode()).hexdigest()
    stored_hash = int_users[email]
    if stored_hash == leaked_hash:
        return "CRITICAL"
    else:
        return "MODERATE"

# Match scoring & collecting (email, severity) pairs.

def get_results(matches, int_users):
    results = []
    for email, password in matches:
        severity = score_match(email, password, int_users)
        results.append((email, severity))

    return results

# Totals per severity.

def print_summary(results, total_employees, total_dump):
    critical_count = 0
    moderate_count = 0
    for email, severity in results:
        if severity == "CRITICAL":
            critical_count += 1
        elif severity == "MODERATE":
            moderate_count += 1
    print("Total Employees: ", total_employees)
    print("Total Dump Entries: ", total_dump)
    print("Matches Detected: ", len(results))
    print("CRITICAL:", critical_count)
    print("MODERATE:", moderate_count)

# Report, severity, string for forced-reset message.

def save_report (results, filepath):
    with open(filepath, "w") as file:
        for email, severity in results:
            file.write(email + ": " + severity + "\n")
        critical_emails = []
        for email, severity in results:
            if severity == "CRITICAL":
                critical_emails.append(email)
        file.write("\n The following accounts need forced reset:\n")

        for email in critical_emails:
            file.write(email + "\n")

# Load, match, score, summarize, report.

def main():
    int_users = load_int_users("int_employees.csv")
    dump = load_ext_dump("ext_dump.csv")
    matches = find_matches(dump, int_users)
    results = get_results(matches, int_users)
    print_summary(results, len(int_users), len(dump))
    save_report(results, "data_leak_report.txt")

main()